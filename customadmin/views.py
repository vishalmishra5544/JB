from django.contrib import messages
from django.http import HttpResponseRedirect
# Create your views here.
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from campus.models import stu_details,comp_details,job_pos
def admin_login(request):
    error=False
    errordescription=''
    try:
        if request.user.is_authenticated:
            return redirect('/')
        if request.method == 'POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            user_obj=User.objects.filter(username=username)
            if not user_obj.exists():
                #messages.info(request,'Account not found')
                error=True
                errordescription='Account not found'
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj=authenticate(username=username,password=password)
            if user_obj and user_obj.is_superuser:
                login(request,user_obj)
                return redirect('/')
            #messages.info(request,'Invalid password')
            error = True
            errordescription = 'Invalid login details'
            return render(request,'customadmin.html',{'error':error,'errordescription':errordescription})
        return render(request,'customadmin.html',{'error':error,'errordescription':errordescription})
    except:
        return render(request,'customadmin.html',{'error':error,'errordescription':errordescription})


def viewstudents(request):
    studentsList=stu_details.objects.all()
    return render(request,'viewstudents.html',{'students':studentsList})

def viewcompanies(request):
    companiesList=comp_details.objects.all()
    return render(request,'viewcompanies.html',{'companies':companiesList})

def viewpostings(request):
    postingsList=job_pos.objects.all()
    return render(request,'viewpostings.html',{'postings':postingsList})