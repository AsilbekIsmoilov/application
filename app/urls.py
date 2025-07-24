from django.urls import path
from .views import *

urlpatterns = [
    path('', index_view, name='index'),
    path('statistics/', statistics, name='statistics'),
    path('report/', report_view, name='report'),
    path('report/download/', download_excel, name='download_excel'),
    path('edit/<int:pk>/', edit_request, name='edit_request'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
