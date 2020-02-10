from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.conf import settings


class Account(models.Model):
    # code нужен для внешних счетов
    code = models.CharField(
        verbose_name='код',
        max_length=30,
        blank=True,
    )
    # null нужен для поддержки внешних счетов
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name='пользователь',
        related_name='account_list',
        on_delete=models.CASCADE,
        null=True,
    )
    # даем возможность заводить
    # несколько счетов в одной валюте
    currency = models.CharField(
        verbose_name='валюта',
        max_length=10,
        default=settings.USD,
        choices=settings.CURRENCY_CHOICES,
    )

    class Meta:
        verbose_name = 'счет'
        verbose_name_plural = 'счета'

    @property
    def balance(self):
        debit = self.operation_list.filter(direction=settings.DEBIT)
        credit = self.operation_list.filter(direction=settings.CREDIT)

        debit_amount = debit.aggregate(total=Sum('amount'))['total'] or Decimal('0')
        credit_amount = credit.aggregate(total=Sum('amount'))['total'] or Decimal('0')

        return debit_amount - credit_amount


