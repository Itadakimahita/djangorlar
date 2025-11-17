# Django modules
from django.core.management.base import BaseCommand
from django.db.models import (
    Q, Count, Avg, Max, Min, Sum, F, Value, Case, When, ExpressionWrapper, DurationField
)
from django.db.models.functions import Concat, ExtractYear
from django.utils.timezone import now, timedelta

# Project modules
from users.models import CustomUser



# 2.1
q_2_1 = CustomUser.objects.filter(is_active=True)

# 2.2
q_2_2 = CustomUser.objects.filter(email__endswith='@gmail.com')

# 2.3
q_2_3 = CustomUser.objects.filter(city='Almaty')

# 2.4
q_2_4 = CustomUser.objects.exclude(city='Almaty')

# 2.5
q_2_5 = CustomUser.objects.filter(salary__gt=500000)

# 2.6
q_2_6 = CustomUser.objects.filter(department='IT', country='Kazakhstan')

# 2.7
q_2_7 = CustomUser.objects.filter(birth_date__isnull=True)

# 2.8
q_2_8 = CustomUser.objects.filter(first_name__istartswith='A')

# 2.9
q_2_9 = CustomUser.objects.count()

# 2.10
q_2_10 = CustomUser.objects.order_by('-date_joined')[:20]

# 2.11
q_2_11 = CustomUser.objects.values_list('city', flat=True).distinct()

# 2.12
q_2_12 = CustomUser.objects.filter(department='Sales').count()

# 2.13
seven_days_ago = now() - timedelta(days=7)
q_2_13 = CustomUser.objects.filter(last_login__gte=seven_days_ago)

# 2.14
q_2_14 = CustomUser.objects.filter(
    Q(first_name__icontains='bek') | Q(last_name__icontains='bek')
)

# 2.15
q_2_15 = CustomUser.objects.filter(salary__range=(300000, 700000))

# 2.16
q_2_16 = CustomUser.objects.filter(department__in=['IT', 'HR', 'Finance'])

# 2.17
q_2_17 = CustomUser.objects.values('department').annotate(count=Count('id'))

# 2.18
q_2_18 = CustomUser.objects.values('department').annotate(count=Count('id')).order_by('-count')

# 2.19
q_2_19 = CustomUser.objects.values('city').annotate(count=Count('id')).order_by('-count')[:5]

# 2.20
q_2_20 = CustomUser.objects.filter(last_login__isnull=True)

# 2.21
q_2_21 = CustomUser.objects.aggregate(avg_salary=Avg('salary'))

# 2.22
q_2_22 = CustomUser.objects.aggregate(max_salary=Max('salary'), min_salary=Min('salary'))

# 2.23
q_2_23 = CustomUser.objects.filter(phone__contains='+7')

# 2.24
q_2_24 = CustomUser.objects.annotate(full_name=Concat('first_name', Value(' '), 'last_name'))

# 2.25
q_2_25 = CustomUser.objects.annotate(
    birth_year=ExtractYear('birth_date')
).order_by('birth_year')

# 2.26
q_2_26 = CustomUser.objects.filter(birth_date__month=5)

# 2.27
q_2_27 = CustomUser.objects.filter(role='manager', salary__gt=400000)

# 2.28
q_2_28 = CustomUser.objects.filter(Q(role='employee') | Q(department='HR'))

# 2.29
q_2_29 = CustomUser.objects.filter(is_active=True).values('city').annotate(count=Count('id'))

# 2.30
q_2_30 = CustomUser.objects.order_by('date_joined')[:10]

# 2.31
q_2_31 = CustomUser.objects.filter(city__startswith='A', salary__gt=300000)

# 2.32
q_2_32 = CustomUser.objects.filter(Q(department__isnull=True) | Q(department=''))

# 2.33
q_2_33 = CustomUser.objects.values('country').annotate(
    users=Count('id'),
    avg_salary=Avg('salary')
)

# 2.34
q_2_34 = CustomUser.objects.filter(is_staff=True).order_by('-last_login')

# 2.35
q_2_35 = CustomUser.objects.exclude(email__icontains='example.com')

# 2.36
avg_salary = CustomUser.objects.aggregate(a=Avg('salary'))['a']
q_2_36 = CustomUser.objects.filter(salary__gt=avg_salary)

# 2.37
q_2_37 = CustomUser.objects.values('email').annotate(count=Count('id')).filter(count__gt=1)

# 2.38
q_2_38 = CustomUser.objects.annotate(
    salary_level=Case(
        When(salary__lt=300000, then=Value('low')),
        When(salary__lte=700000, then=Value('medium')),
        default=Value('high')
    )
).order_by('salary_level')

# 2.39
current_year = now().year
q_2_39 = CustomUser.objects.filter(date_joined__year=current_year)

# 2.40
q_2_40 = CustomUser.objects.values('department').annotate(total_payroll=Sum('salary'))

# 2.41
q_2_41 = CustomUser.objects.filter(department='IT', last_login__isnull=True)

# 2.42
q_2_42 = CustomUser.objects.filter(
    country='Kazakhstan'
).filter(Q(city__isnull=True) | Q(city=''))

# 2.43
q_2_43 = CustomUser.objects.filter(birth_date__lt='1990-01-01', salary__isnull=False)

# 2.44
q_2_44 = CustomUser.objects.annotate(
    years_since_joined=ExpressionWrapper(now() - F('date_joined'), output_field=DurationField())
)

# 2.45
q_2_45 = CustomUser.objects.filter(
    department='Sales',
    email__endswith='@gmail.com',
    salary__gt=350000
)

# 2.46
q_2_46 = CustomUser.objects.order_by('country', '-salary')

# 2.47
q_2_47 = CustomUser.objects.values('role').annotate(count=Count('id')).filter(count__gt=100)

# 2.48
q_2_48 = CustomUser.objects.filter(last_login__lt=F('date_joined'))

# 2.49
q_2_49 = CustomUser.objects.annotate(
    is_senior=Case(
        When(birth_date__lt='1985-01-01', then=True),
        default=False
    )
)

# 2.50
q_2_50 = CustomUser.objects.values('department').annotate(
    avg_salary=Avg('salary'),
    count=Count('id')
).filter(count__gte=20).order_by('-avg_salary')
