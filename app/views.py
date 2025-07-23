from django.shortcuts import render, redirect
from django.contrib import messages
from app.forms import RequestLogForm
from app.models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.db.models import Count
from django.http import HttpResponse
import pandas as pd
from datetime import datetime, time
from django.shortcuts import render, get_object_or_404, redirect


def index_view(request):
    selected_operator_id = request.session.get('selected_operator_id')
    urls = Urls.objects.all()
    if request.method == 'POST':
        form = RequestLogForm(request.POST)
        if form.is_valid():
            operator_id = form.cleaned_data['operator'].id
            request.session['selected_operator_id'] = operator_id
            form.save()
            messages.success(request, "✅ Заявка отправлена!")
            return redirect('index')
    else:
        if selected_operator_id:
            form = RequestLogForm(initial={'operator': selected_operator_id})
        else:
            form = RequestLogForm()
        overall_stats = (
        RequestLog.objects.values('theme__title')
        .annotate(count=Count('id'))
        .order_by('-count')
    )
    total_count = sum(row['count'] for row in overall_stats)


    context = {
        'overall_stats': overall_stats,
        'form': form,
        'selected_operator_id': selected_operator_id,
        'total_count': total_count,
        'urls':urls,
    }
    return render(request, 'app/index.html', context)

def statistics(request):
    operator_id = request.GET.get('operator')
    theme_id = request.GET.get('theme')
    phone_num = request.GET.get('phone_num')

    records = RequestLog.objects.all().select_related('operator', 'theme')

    if operator_id:
        records = records.filter(operator_id=operator_id)

    if theme_id:
        records = records.filter(theme_id=theme_id)

    if phone_num:
        records = records.filter(phone_num__icontains=phone_num)

    
        

    paginator = Paginator(records.order_by('-created_at'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'records': page_obj,
        'operators': Operator.objects.all(),
        'themes': Theme.objects.all(),
        'selected_operator': operator_id,
        'selected_theme': theme_id,
        'selected_phone': phone_num,
    }
    return render(request, 'app/statistics.html', context)


@login_required
def report_view(request):
    overall_stats = (
        RequestLog.objects.values('theme__title')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    total_count = 0
    theme_stats = []

    if start_date and end_date:
        try:
            start = datetime.strptime(start_date, '%Y-%m-%d')
            end = datetime.strptime(end_date, '%Y-%m-%d')

            start_datetime = datetime.combine(start.date(), time.min)
            end_datetime = datetime.combine(end.date(), time.max)

            queryset = RequestLog.objects.filter(created_at__range=(start_datetime, end_datetime))

            total_count = queryset.count()
            theme_stats = (
                queryset
                .values('theme__title')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
        except ValueError:
            pass

    context = {
        'overall_stats': overall_stats,
        'total_count': total_count,
        'theme_stats': theme_stats,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'app/report.html', context)

@login_required
def download_excel(request):
    stats = RequestLog.objects.values('theme__title').annotate(count=Count('id')).order_by('theme__title')

    df = pd.DataFrame(list(stats))
    df.rename(columns={'theme__title': 'Тема', 'count': 'Сони'}, inplace=True)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=общая статистика.xlsx'
    df.to_excel(response, index=False)
    return response



def edit_request(request, pk):
    instance = get_object_or_404(RequestLog, pk=pk)
    if request.method == 'POST':
        form = RequestLogForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('statistics')
    else:
        form = RequestLogForm(instance=instance)
    
    return render(request, 'app/edit_request.html', {'form': form,'instance': instance })
