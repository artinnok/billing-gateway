from decimal import Decimal

from django.db import transaction
from django.conf import settings

from billing.models import Operation, Account, Payment


def calculate_fee(from_account, to_account, amount):
    if from_account.user == to_account.user:
        return Decimal('0')
    return Decimal(amount) * settings.DEFAULT_FEE_PERCENT / Decimal('100')


def transfer_money(from_account_id, to_account_id, amount, fee):
    from_account = Account.objects.get(id=from_account_id)
    to_account = Account.objects.get(id=to_account_id)
    amount = Decimal(amount)
    fee = Decimal(fee)

    with transaction.atomic():
        payment = Payment.objects.create()

        # берем комиссию и считаем остаток средств
        fee = _take_fee(
            account=from_account,
            fee=fee,
            payment=payment,
        )
        rest_amount = amount - fee

        # реализуем стандартное двойное начисление
        _make_payment(
            from_account=from_account,
            to_account=to_account,
            amount=rest_amount,
            payment=payment,
        )

    return {'fee': fee, 'rest_amount': rest_amount, 'payment': payment}


def _take_fee(account, fee, payment):
    if not fee:
        return Decimal('0')

    internal_account = Account.objects.get(
        code=settings.INTERNAL,
        currency=account.currency,
    )

    _make_payment(account, internal_account, fee, payment, settings.FEE)

    return fee


def _make_payment(from_account, to_account, amount, payment, kind=settings.TRANSFER):
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
