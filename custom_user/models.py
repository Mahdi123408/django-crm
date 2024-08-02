from django.db import models
from jdatetime import datetime, timedelta
from custom_auth.models import User
from my_methods.convertors import price_split


class TimeWorkUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کارمند')
    date = models.CharField(max_length=200, verbose_name='روز کاری')
    start_time = models.CharField(max_length=200, verbose_name='ساعت شروع')
    end_time = models.CharField(max_length=200, null=True, blank=True, verbose_name='ساعت پایان')
    time_work = models.CharField(max_length=50, editable=False, verbose_name='مقدار ساعت کار کارمند در این روز')

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'ساعات کار کاربر'
        verbose_name_plural = 'ساعات کار کاربران'

    def time_work_user(self):
        time_work = datetime.strptime(self.end_time, '%H:%M:%S') - datetime.strptime(self.start_time, '%H:%M:%S')
        return str(time_work)

    def save(self, *args, **kwargs):
        self.time_work = self.time_work_user()
        super(TimeWorkUser, self).save(*args, **kwargs)


class UserExports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کارمند')
    price_count = models.IntegerField(verbose_name='مقدار برداشتی به تومان')
    date = models.CharField(max_length=200, verbose_name='تاریخ برداشت')
    description = models.TextField(null=True, blank=True, verbose_name='توضیحات ( اختیاری )')

    def __str__(self):
        return str(str(self.user) + self.date)

    class Meta:
        verbose_name = 'برداشت کاربر'
        verbose_name_plural = 'برداشت های کاربران'

    def price_count_split(self):
        return price_split(self.price_count)


class UserWorksHourRequests(models.Model):
    user = models.ForeignKey(User, primary_key=True, unique=True, on_delete=models.CASCADE, verbose_name='کارمند')
    date = models.CharField(max_length=200)
    start_time = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'درخواست کاربر'
        verbose_name_plural = 'درخواست های کاربران های کاربران'
