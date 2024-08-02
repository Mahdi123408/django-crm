from django.shortcuts import render, redirect
from django.views import View

from custom_auth.models import User
from jdatetime import datetime, timedelta
from my_methods.auth import check_auth
from my_methods.convertors import price_split
from .models import UserWorksHourRequests, TimeWorkUser
from custom_admin.models import PriceDay, PriceExportDay


class UserView(View):
    def get(self, request):
        mes = None
        if 'mes' in request.session:
            mes = request.session['mes']
            del request.session['mes']
        check_user = check_auth(request)
        if check_user[0]:
            if check_user[1].is_admin:
                this_month_price_day = PriceDay.get_this_month(self)
                this_month_export_price_day = PriceExportDay.get_this_month(self)
                get_this_month_sum_split_price = PriceDay.get_this_month_sum_split(self)
                get_this_month_sum_split_export = PriceExportDay.get_this_month_sum_split(self)
                total_price = PriceDay.get_this_month_sum(self) - PriceExportDay.get_this_month_sum(self)
                context = {
                    'user': check_user[1],
                    'mes': mes,
                    'this_month_price_day': this_month_price_day,
                    'this_month_export_price_day': this_month_export_price_day,
                    'this_month_export_price_sum': get_this_month_sum_split_export,
                    'this_month_price_sum': get_this_month_sum_split_price,
                    'total_price': price_split(total_price),
                }
                return render(request, 'admin/admin.html', context)
            context = {
                'user': check_user[1],
                'mes': mes,
            }
            return render(request, 'user/user_view/user_view.html', context)
        else:
            request.session['mes'] = 'ابتدا وارد شوید'
            return redirect('login')

    def post(self, request):
        check_user = check_auth(request)
        if check_user[0]:
            if 'start' in request.POST:
                userneame = request.POST['start']
                user = User.objects.filter(pk=userneame).first()
                if user:
                    check_user = UserWorksHourRequests.objects.filter(user=user).first()
                    if check_user:
                        request.session[
                            'mes'] = 'شما در حال حاضر کار خود را شروع کرده اید برای شروع مجدد باید درخواست قبلی را پایان داده و دوباره شروع کنید . در صورتی که قصد ویرایش ساعت دارید به آقای عباسی اطلاع دهید .'
                        return redirect('user')
                    else:
                        date = datetime.now()
                        UserWorksHourRequests.objects.create(user=user,
                                                             date=date.strftime('%Y/%m/%d'),
                                                             start_time=date.strftime('%H:%M:%S'),
                                                             )
                        request.session[
                            'mes'] = f'با موفقیت ساعت کاری شما در لحظه {date.strftime('%Y/%m/%d')}-{date.strftime('%H:%M:%S')} ثبت شد . '
                        return redirect('user')
                else:
                    request.session['mes'] = 'کارمند یافت نشد'
                    return redirect('user')
            elif 'end' in request.POST:
                userneame = request.POST['end']
                user = User.objects.filter(pk=userneame).first()
                if user:
                    check_user = UserWorksHourRequests.objects.filter(user=user).first()
                    if check_user:
                        date = datetime.now()
                        if (date - datetime.strptime(check_user.date + ' ' + check_user.start_time,
                                                     '%Y/%m/%d %H:%M:%S')).seconds / 3600 <= 6:
                            TimeWorkUser.objects.create(user=user,
                                                        date=check_user.date,
                                                        start_time=check_user.start_time,
                                                        end_time=date.strftime('%H:%M:%S'),
                                                        )

                            request.session[
                                'mes'] = f'ساعت کاری شما با مشخصات ذیل ثبت شد : تاریخ : {check_user.date} زمان شروع : {check_user.start_time}  زمان پایان : {date.strftime('%H:%M:%S')}'
                            check_user.delete()
                            return redirect('user')
                        else:
                            request.session['mes'] = 'حد اکثر ساعت کاری مجاز در یک شیفت 6 ساعت میباشد و درخواست شما بیش از این مقدار است . ساعت شروع شما پاک شده و اگر اعتراضی دارید با آقای عباسی مطرح کنید'
                            check_user.delete()
                            return redirect('user')
                    else:
                        request.session['mes'] = 'شما ساعت کاری را شروع نکردید که بخواهید به آن خاتمه بدهید'
                        return redirect('user')
                else:
                    request.session['mes'] = 'کارمند یافت نشد'
                    return redirect('user')
        else:
            request.session['mes'] = 'ابتدا وارد شوید'
            return redirect('login')
