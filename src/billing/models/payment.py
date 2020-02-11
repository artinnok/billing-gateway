from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property


class Payment(models.Model):
    from_account = models.ForeignKey(
        'billing.Account',
        verbose_name='счет отправителя',
        related_name='from_payment_list',
        on_delete=models.CASCADE,
    )
    to_account = models.ForeignKey(
        'billing.Account',
        verbose_name='счет получателя',
        related_name='to_payment_list',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=9,
        decimal_places=3,
    )
    fee = models.DecimalField(
        verbose_name='комиссия',
        max_digits=9,
        decimal_places=3,
    )
    status = models.CharField(
        verbose_name='статус',
        max_length=10,
        choices=settings.STATUS_CHOICES,
    )

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'

    @cached_property
    def rest_amount(self):
        return self.amount - self.fee

    @staticmethod
    def calculate_fee(from_account, to_account, amount):
        if from_account.user == to_account.user:
            return Decimal('0')
        return Decimal(amount) * settings.DEFAULT_FEE_PERCENT / Decimal('100')
