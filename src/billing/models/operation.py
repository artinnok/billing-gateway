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
        return {'amount': self.payment.fee}
