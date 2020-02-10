import django
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model

django.setup()

from billing.models import Account, Payment
from billing.utils import make_double_accrual, calculate_fee


USER = get_user_model()


def create_init_account(email, password):
    with transaction.atomic():
        user = USER.objects.create_user(
            email=email,
            password=password,
        )

        for currency in settings.DEFAULT_CURRENCY_LIST:
            account = Account.objects.create(
                user=user,
                currency=currency,
            )
            if currency != settings.USD:
                continue

            internal_account = Account.objects.get(
                code=settings.INTERNAL,
                currency=currency,
            )
            payment = Payment.objects.create(
                user=user,
                status=settings.INITIATED,
            )

            make_double_accrual(
                payment=payment,
                from_account=internal_account,
                to_account=account,
                amount=settings.DEFAULT_USD_BALANCE,
                fee=settings.ZERO_FEE,
            )


def transfer_money(payment_id, from_account_id, to_account_id, amount):
    payment = Payment.objects.get(id=payment_id)
    from_account = Account.objects.get(id=from_account_id)
    to_account = Account.objects.get(id=to_account_id)

    fee = calculate_fee(
        from_account=from_account,
        to_account=to_account,
        amount=amount,
    )
    make_double_accrual(
        payment=payment,
        from_account=from_account,
        to_account=to_account,
        amount=amount,
        fee=fee,
    )
