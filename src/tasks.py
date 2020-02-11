import django
from django.conf import settings
from django.db import transaction
from django.contrib.auth import get_user_model

django.setup()

from billing.models import Account, Payment
from billing.utils import complete_payment


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
                from_account=internal_account,
                to_account=account,
                amount=settings.DEFAULT_USD_BALANCE,
                fee=settings.ZERO_FEE,
                status=settings.INITIATED,
            )

            complete_payment(payment)


def transfer_money(payment_id):
    payment = Payment.objects.get(id=payment_id)

    complete_payment(payment)
