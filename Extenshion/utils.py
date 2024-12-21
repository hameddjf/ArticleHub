from . import jalali
# import jalali ==> کار نمیکنه
from django.utils import timezone

def persian_numsers_converter(mystr):
    numbers = {
        '0' : '۰' ,
        '1' : '۱' ,
        '2' : '۲' ,
        '3' : '۳' ,
        '4' : '۴' ,
        '5' : '۵' ,
        '6' : '۶' ,
        '7' : '۷' ,
        '8' : '۸' ,
        '9' : '۹' ,
    }
    for e , p in numbers.items():
        mystr = mystr.replace(e , p)
    return mystr

def jalali_converter(time):
    jmonth = ['فروردین' , 'اردیبهشت' , 'خرداد' , 'تیر' , 'مرداد' , 'ِشهریور' , 'مهر' , 'ابان' , 'اذر' , 'دی' , 'بهمن' , 'اسفند']

    time = timezone.localtime(time) # برابر قرار دادن تایم ثبت شده برای مقاله با تایمی که از پنل ادمین وارد تغییرات مقاله میشی برابر میکنه ... ی تایم متغییر نمیزاره

    time_to_str = "{},{},{}".format(time.year,time.month,time.day) # دریافت زمان حال و تبدیل ان به استرینگ
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple() # دریافت زمان استرینگ شده و تدیل ان به زمان شمسی 

    time_to_list = list(time_to_tuple)
    for index , month in enumerate(jmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    output = "{} {} {} , ساعت {}:{}".format(
        time_to_list[2],
        time_to_list[1],
        time_to_list[0],
        time.hour , 
        time.minute,
        
            )

    return persian_numsers_converter(output)