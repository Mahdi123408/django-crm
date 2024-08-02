from django.db import models
from my_methods.convertors import price_split as price_split2
from jdatetime import datetime, timedelta


class PriceDay(models.Model):
    price = models.IntegerField(verbose_name='درآمد')
    day = models.CharField(max_length=100, verbose_name='روز')

    def __str__(self):
        return f'{self.day} - {price_split2(self.price)}'

    class Meta:
        verbose_name = 'درآمد در روز'
        verbose_name_plural = 'درآمد های روزانه'

    def get_this_month(self):
        month = datetime.now().strftime('%Y/%m')
        l = []
        time_works = PriceDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                l.append(time_work)
        return l

    def price_split(self):
        return price_split2(self.price)

    def get_this_month_sum(self):
        month = datetime.now().strftime('%Y/%m')
        z = 0
        time_works = PriceDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                z += time_work.price
        return z

    def get_this_month_sum_split(self):
        month = datetime.now().strftime('%Y/%m')
        z = 0
        time_works = PriceDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                z += time_work.price
        return price_split2(z)


class PriceExportDay(models.Model):
    day = models.CharField(max_length=100, verbose_name='روز')
    price = models.IntegerField(verbose_name='هزینه')
    description = models.TextField(verbose_name='توضیحات')

    def __str__(self):
        return f'{self.day} - {price_split2(self.price)}'

    class Meta:
        verbose_name = 'هزینه در روز'
        verbose_name_plural = 'هزینه های روزانه'

    def get_this_month(self):
        month = datetime.now().strftime('%Y/%m')
        l = []
        time_works = PriceExportDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                l.append(time_work)
        return l

    def price_split(self):
        return price_split2(self.price)

    def get_this_month_sum(self):
        month = datetime.now().strftime('%Y/%m')
        z = 0
        time_works = PriceExportDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                z += time_work.price
        return z

    def get_this_month_sum_split(self):
        month = datetime.now().strftime('%Y/%m')
        z = 0
        time_works = PriceExportDay.objects.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.day, '%Y/%m/%d').strftime('%Y/%m'):
                z += time_work.price
        return price_split2(z)
