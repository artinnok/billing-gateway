from decimal import Decimal

from django.db import models
from django.conf import settings
from django.utils.functional import cached_property
from django.core.exceptions import ObjectDoesNotExist


class Payment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        related_name='payment_list',
        on_delete=models.CASCADE,
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
    def sender_account(self):
        return self._get_sender_receiver(settings.CREDIT)

    @cached_property
    def receiver_account(self):
        return self._get_sender_receiver(settings.DEBIT)

    def _get_sender_receiver(self, direction):
        operation = self.operation_list.get(
            direction=direction,
            kind=settings.TRANSFER,
        )
        return operation.account

    @cached_property
    def fee(self):
        try:
            return self.operation_list.get(
                direction=settings.CREDIT,
                kind=settings.FEE,
            ).amount
        except ObjectDoesNotExist:
            return Decimal('0')

    @cached_property
    def amount(self):
        operation = self.operation_list.get(
            direction=settings.CREDIT,
            kind=settings.TRANSFER,
        )
        return operation.amount
