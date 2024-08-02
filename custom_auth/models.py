from django.db import models
from jdatetime import datetime, timedelta
from my_methods.convertors import price_split


class User(models.Model):
    username = models.CharField(max_length=80, primary_key=True, unique=True, db_index=True, verbose_name='نام کاربری')
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی کارمند')
    price = models.IntegerField(verbose_name='درآمد به ازای هر ساعت', db_index=True)
    active = models.BooleanField(default=False, verbose_name='فعال یا غیر فعال')
    password = models.CharField(max_length=100, verbose_name='رمز عبور')
    is_admin = models.BooleanField(default=False, verbose_name='ادمین است یا خیر')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندان'

    def check_password(self, password):
        if self.password == password:
            return True
        else:
            return False

    def user_works(self):
        return self.timeworkuser_set.all()

    def user_exports(self):
        return self.userexports_set.all()

    def this_month_user_works(self):
        month = datetime.now().strftime('%Y/%m')
        l = []
        time_works = self.timeworkuser_set.all()
        for time_work in time_works:
            if month == datetime.strptime(time_work.date, '%Y/%m/%d').strftime('%Y/%m'):
                l.append(time_work)
        return l

    def this_month_user_exports(self):
        month = datetime.now().strftime('%Y/%m')
        l = []
        user_exports = self.userexports_set.all()
        for user_export in user_exports:
            if month == datetime.strptime(user_export.date, '%Y/%m/%d').strftime('%Y/%m'):
                l.append(user_export)
        return l

    def user_price_month(self):
        price_of_hour = self.price
        time_works_month = self.this_month_user_works()
        price_month = 0
        total_time_works_month = timedelta()  # Initialize with zero timedelta

        for time_work in time_works_month:
            # Convert string to timedelta
            hours, minutes, seconds = map(int, time_work.time_work.split(':'))
            time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            total_time_works_month += time_delta  # Add timedelta to total

        # Calculate the total price based on total hours worked
        total_hours = total_time_works_month.total_seconds() / 3600  # Convert total timedelta to hours
        price_month = int(total_hours) * int(price_of_hour)

        return price_split(price_month)

    def user_price_month_int(self):
        price_of_hour = self.price
        time_works_month = self.this_month_user_works()
        price_month = 0
        total_time_works_month = timedelta()  # Initialize with zero timedelta

        for time_work in time_works_month:
            # Convert string to timedelta
            hours, minutes, seconds = map(int, time_work.time_work.split(':'))
            time_delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            total_time_works_month += time_delta  # Add timedelta to total

        # Calculate the total price based on total hours worked
        total_hours = total_time_works_month.total_seconds() / 3600  # Convert total timedelta to hours
        price_month = int(total_hours) * int(price_of_hour)

        return int(price_month)

    def user_price_exports_month(self):
        user_exports = self.this_month_user_exports()
        price_month = 0
        for user_export in user_exports:
            price_month += user_export.price_count
        return price_split(price_month)

    def user_price_exports_month_int(self):
        user_exports = self.this_month_user_exports()
        price_month = 0
        for user_export in user_exports:
            price_month += user_export.price_count
        return int(price_month)

    def price_split_user(self):
        base_price = str(self.price)
        counter = len(base_price) - 1
        counter2 = 0
        price_export = ''
        while counter >= 0:
            if counter2 < 3:
                price_export = base_price[counter] + price_export
                counter -= 1
                counter2 += 1
            else:
                price_export = base_price[counter] + ',' + price_export
                counter -= 1
                counter2 = 1
        return price_export

    def this_month_real_price_user_int(self):
        this_month_base_price = int(self.user_price_month_int())
        this_month_export_user_price = int(self.user_price_exports_month_int())
        return this_month_base_price - this_month_export_user_price

    def this_month_real_price_user_split(self):
        this_month_base_price = int(self.user_price_month_int())
        this_month_export_user_price = int(self.user_price_exports_month_int())
        return price_split(this_month_base_price - this_month_export_user_price)
