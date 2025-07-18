from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count
from django.contrib import messages
from app.forms import RequestLogForm
from app.models import *

def short_name(full_name):
    """FIO dan faqat 2 ta birinchi so‘zni ajratish"""
    parts = full_name.split()
    return " ".join(parts[:2]) if len(parts) >= 2 else full_name

def index(request):
    urls = Urls.objects.all()
    operator_id = ""
    selected_operator_id = request.session.get('last_operator_id')

    if request.method == 'GET' and request.GET.get('operator_id'):
        selected_operator_id = request.GET['operator_id']
        request.session['last_operator_id'] = selected_operator_id

    initial_data = {}
    if selected_operator_id:
        initial_data['operator'] = selected_operator_id
    form = RequestLogForm(initial=initial_data)

    if request.method == 'POST':
        form = RequestLogForm(request.POST)
        if form.is_valid():
            selected_operator = form.cleaned_data['operator']
            selected_operator_id = selected_operator.id
            request.session['last_operator_id'] = selected_operator_id
            form.save()
            messages.success(request, "✅ Заявка успешно отправлена!")
            return redirect('index')

    selected_operator = None
    try:
        selected_operator = Operator.objects.get(id=selected_operator_id)
    except Operator.DoesNotExist:
        pass

    today = timezone.now().date()
    now = timezone.now()

    raw_top_10 = (
        RequestLog.objects
        .filter(created_at__date=today)
        .values('operator__id', 'operator__fio')
        .annotate(total=Count('id'))
        .order_by('-total')[:10]
    )

    top_10_list = []
    top_10_ids = []

    for entry in raw_top_10:
        top_10_list.append({
            'id': entry['operator__id'],
            'fio': short_name(entry['operator__fio']),
            'count': entry['total']
        })
        top_10_ids.append(entry['operator__id'])

    # Rank
    top_10_rank = None
    if selected_operator and selected_operator.id in top_10_ids:
        top_10_rank = top_10_ids.index(selected_operator.id) + 1

    daily_status = RequestLog.objects.filter(
        operator_id=selected_operator_id,
        created_at__date=today
    ).count()

    monthly_status = RequestLog.objects.filter(
        operator_id=selected_operator_id,
        created_at__year=now.year,
        created_at__month=now.month
    ).count()

    return render(request, 'app/index.html', {
        'form': form,
        'operator_id': selected_operator.operator_id if selected_operator else "",
        'top_10_rank': top_10_rank,
        'daily_status': daily_status,
        'monthly_status': monthly_status,
        'operators': Operator.objects.all(),
        'top_10_list': top_10_list,
        'urls': urls,
        'selected_operator_id': selected_operator_id,
    })
