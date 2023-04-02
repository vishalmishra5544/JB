from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('logout/', views.pagelogout, name='logout'),
    path('student/student_register/', views.student_register, name='student_register'),
    path('student/student_login/', views.student_login, name='student_login'),
    path('student/student_login/usd/', views.usd, name='usd'),
    path('student/student_login/applyjob/', views.applyjob, name='apply'),
    path('student/student_login/applyjob/<str:opt>/', views.apply, name='apply1'),
    path('student/student_login/dispstu/', views.dispstu, name='dispstu'),
    path('student/student_login/trackapplicationstatus/', views.trackapplicationstatus, name='trackapplicationstatus'),
    path('student/student_login/UploadResume/', views.UploadResume, name='UploadResume'),
    path('company/company_register/', views.company_register, name='company_register'),
    path('company/company_login/', views.company_login, name='company_login'),
    path('company/company_login/ccd/', views.ccd, name='ccd'),
    path('company/company_login/jp/', views.jobpos, name='jp'),
    path('company/company_login/jd/', views.jd, name='jd'),
    path('company/company_login/deletevacan/', views.deletevacan, name='deletevacn'),
    path('company/company_login/viewpos/', views.viewpos, name='viewpos'),
    path('company/company_login/selectstu/', views.selectstu, name='sstu'),
    path('company/company_login/selectstu/<int:jobid>/<str:opt>/', views.stumail, name="sm")
]
