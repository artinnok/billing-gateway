from django.db import models
from django.conf import settings


class Operation(models.Model):
    account = models.ForeignKey(
        'billing.Account',
        verbose_name='счет',
        related_name='operation_list',
        on_delete=models.CASCADE,
    )
    payment = models.ForeignKey(
        'billing.Payment',
        verbose_name='платеж',
        related_name='operation_list',
        on_delete=models.CASCADE,
    )
    direction = models.CharField(
        verbose_name='направление',
        max_length=10,
        choices=settings.DIRECTION_CHOICES,
    )
    kind = models.CharField(
        verbose_name='тип',
        max_length=10,
        choices=settings.KIND_CHOICES,
    )
    amount = models.DecimalField(
        verbose_name='сумма',
        max_digits=9,
        decimal_places=3,
    )

    class Meta:
        verbose_name = 'операция'
        verbose_name_plural = 'операции'

    @property
    def fee(self):
        amount = self.payment.fee
        # с пополнений счета платит комиссию другой
        if self.direction == settings.DEBIT:
            amount = settings.ZERO_FEE

        return str(amount)

    @property
    def sender(self):
        return self._get_sender_receiver('from_account')

    @property
    def receiver(self):
        return self._get_sender_receiver('to_account')

    def _get_sender_receiver(self, account_name):
        account = getattr(self.payment, account_name)

        if account.user:
            username = account.user.email
        else:
            username = account.code

        return username
