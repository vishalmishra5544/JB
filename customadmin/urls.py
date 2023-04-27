from django.urls import path
from . import views
urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('student', views.viewstudents, name='viewstudents'),
    path('companies', views.viewcompanies, name='viewcompanies'),
    path('postings', views.viewpostings, name='viewpostings'),
]