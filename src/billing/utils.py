from decimal import Decimal

from django.db import transaction
from django.conf import settings

from billing.models import Operation, Account


def complete_payment(payment):
    with transaction.atomic():
        # берем комиссию и считаем остаток средств
        _take_fee(
            account=payment.from_account,
            fee=payment.fee,
            payment=payment,
        )

        # реализуем стандартное двойное начисление
        _make_double_accrual(
            from_account=payment.from_account,
            to_account=payment.to_account,
            amount=payment.rest_amount,
            payment=payment,
        )

        payment.status = settings.COMPLETED
        payment.save()

    return payment


def _take_fee(account, fee, payment):
    if not fee:
        return Decimal('0')

    internal_account = Account.objects.get(
        code=settings.INTERNAL,
        currency=account.currency,
    )

    _make_double_accrual(account, internal_account, fee, payment, settings.FEE)

    return fee


def _make_double_accrual(from_account, to_account, amount, payment, kind=settings.TRANSFER):
    Operation.objects.create(
        account=from_account,
        payment=payment,
        direction=settings.CREDIT,
        amount=amount,
        kind=kind,
    )
    Operation.objects.create(
        account=to_account,
        payment=payment,
        direction=settings.DEBIT,
        amount=amount,
        kind=kind,
    )

    return payment
