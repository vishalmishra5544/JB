from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import Student_SignUpForm,UsdForm,dispstuForm,company_SignUpForm,ccdForm,jobposForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import CreateView
from .models import stu_details,comp_details,job_pos,applied_jobs
from resumeparser.models import Resume
#from django.core.mail import EmailMessage
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

# Create your views here
def  student_login(request):
    if request.user.is_authenticated and request.user.groups.filter(name='student').exists() or request.user.is_superuser:
        return render(request,'campus/stulog.html')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.groups.filter(name='student').exists():
             return render(request, 'campus/stulog.html', {'form': form})
            else:
                logout(request)
                return render(request, 'campus/student_login.html', {'form': form})
        else:
            return render(request, 'campus/student_login.html', {'form': form})


    else:
        form = AuthenticationForm()
        return render(request, 'campus/student_login.html', {'form': form})

def  home(request):
    studentUsers=stu_details.objects.values_list('username', flat=True)
    print(studentUsers)
    companyUsers=comp_details.objects.values_list('username',flat=True)
    return render(request,'campus/home.html',{"studentUsers":studentUsers,"companyUsers":companyUsers})

def pagelogout(request):
        logout(request)
        return redirect('http://127.0.0.1:8000/')


def student_register(request):
    if request.method == 'POST':
        form = Student_SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            group = Group.objects.get(name='student')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('http://127.0.0.1:8000/student/student_login/')

        else:
            return render(request, 'campus/register.html', {'form': form})
    else:
        form =Student_SignUpForm()
        return render(request, 'campus/register.html', {'form': form})

#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='Student').count() == 1)
def usd(request):
 if  request.user.is_authenticated and request.user.groups.filter(name='student').exists() or request.user.is_superuser:
    if request.method == "POST":
        count=0
        cnter=int(count)
        print(cnter+1)
        form=UsdForm(request.POST)
        print(cnter + 1)
        print(form)
        if form.is_valid():
            print(cnter + 1)
            stu = request.user.username
            post = stu_details.objects.filter(username=stu)
            skills=request.POST.get('skills')
            experience=request.POST.get('experience')
            y=request.POST.get('phone_number')
            e=request.POST.get('email')
            b=request.POST.get('branch')
            print(cnter + 1)
            j=post[0]
            print(cnter + 1)
            j.phone_number = y
            j.email=e
            j.branch=b
            j.skills=skills
            j.experience=experience
            print(cnter + 1)
            j.save()
            print(cnter + 1)
            return redirect('campus/student/student_login/dispstu')
        else:
            return redirect('/')
    else:
        stu = request.user.username
        post = stu_details.objects.filter(username=stu)
        y = post[0].phone_number
        e=post[0].email
        b = post[0].branch
        skills=post[0].skills
        experience=post[0].experience
        form=UsdForm()
        context={'form': form,'y':y,'e':e,'b':b,'skills':skills,'experience':experience}
        return render(request, 'campus/usd.html',context)
 else:
     return HttpResponse("<h1>u r not logged in</h1>")



def dispstu(request):
    if request.user.is_authenticated or request.user.is_superuser:
        stu = request.user.username
        reqdPost = stu_details.objects.filter(username=stu)
        post=reqdPost[0]
        form=dispstuForm()
        return render(request, 'campus/dispstu.html', {'form': form, 'post': post})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")



def UploadResume(request):
    return redirect('http://127.0.0.1:8000/resume')

def trackapplicationstatus(request):
    if request.user.is_authenticated and request.user.groups.filter(name='student').exists() or request.user.is_superuser:
      s=""
      y=[]
      if request.method == "POST":
        print("hi")
        jobid=request.POST.get("salary")
        x = request.user.username
        status = applied_jobs.objects.filter(job_id=jobid, student_id=x)
        if(len(status)>0):
            status=status[0].status
            y = job_pos.objects.filter(job_id=jobid)
        print(y)
        if(len(y)==0):
            s="You haven't applied to job"
            print("failed",s)
            return render(request, 'campus/trackapplicationstatus.html',{'s':s})
        else:
            return render(request, 'campus/trackapplicationstatus.html', {'y': y, 's': s,'status':status})
      else:
          return render(request, 'campus/trackapplicationstatus.html', { 'y':y,'s': s,})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")



def company_register(request):
    if request.method == 'POST':
        form = company_SignUpForm(request.POST)
        if form.is_valid():
            user=form.save()
            group = Group.objects.get(name='company')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            a=comp_details()
            a.username=request.POST.get('username')
            a.company_name=request.POST.get('company_name')
            a.email=request.POST.get('email')
            a.est_year=request.POST.get('est_year')
            a.type=request.POST.get('type')
            a.about=request.POST.get('about')
            a.hr_name=request.POST.get('hr_name')
            a.hr_phn=request.POST.get('hr_phn')
            a.headquaters=request.POST.get('headquaters')
            a.save()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            return render(request, 'campus/register1.html', {'form': form})

    else:
        form =company_SignUpForm()
        return render(request, 'campus/register1.html', {'form': form})



def  company_login(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        return render(request,'campus/comlog.html')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if request.user.groups.filter(name='company').exists():
             return render(request, 'campus/comlog.html', {'form': form})
            else:
                logout(request)
                return render(request, 'campus/company_login.html', {'form': form})
        else:
            return render(request, 'campus/company_login.html', {'form': form})
    else:
        form = AuthenticationForm()
        return render(request, 'campus/company_login.html', {'form': form})




def ccd(request):
 if  request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
    if request.method == "POST":
            form=ccdForm(request.POST)
            print(form)
            if form.is_valid():
                stu = request.user.username
                post = comp_details.objects.filter(username=stu)
                x= request.POST.get('hr_name')
                y=request.POST.get('hr_phn')
                z=request.POST.get('about')
                j=post[0]
                j.hr_name =x
                j.hr_phn = y
                j.about=z
                j.save()
                return render(request, 'campus/comlog.html')

    else:
        stu = request.user.username
        post = comp_details.objects.filter(username=stu)
        x = post[0].hr_name
        x=str(x)
        y = post[0].hr_phn
        z=post[0].about
        form=ccdForm()
        return render(request, 'campus/ccd.html', {'form': form,'x':x,'y':y,'z':z})
 else:
     return HttpResponse("<h1>u r not logged in</h1>")



def jobpos(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        if request.method == "POST":
            form = jobposForm(request.POST)
            if form.is_valid():
                    model_instance = form.save(commit=False)
                    model_instance.save()
                    return render(request,'campus/comlog.html')
            else:
                return render(request, 'campus/jobpos.html', {'form': form})
        else:
            form = jobposForm()
            x = request.user.username
            y = comp_details.objects.filter(username=x)
            y = str(y[0].company_name)
            y=y.split()
            y1=""
            for i in y:
                y1=y1+"_"+i
            y1=y1[1:len(y1)]
            print(y)

            return render(request, 'campus/jobpos.html', {'form': form,'x':x,'y':y1})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")

def jd(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        if request.method == "POST":
                    s=""
                    print("hiiiiiii")
                    book=job_pos.objects.filter(job_id=request.POST.get("job_id"))
                    print(len(book))
                    if(len(book)!=1):
                        s="Wrong job id try again"
                        return render(request, 'campus/jd.html',{'s':s})
                    book=book[0]
                    book.designation=request.POST.get("designation")
                    book.salary=request.POST.get("salary")
                    book.bond_years=request.POST.get("bond_years")
                    book.information_technology=request.POST.get("information_technology")
                    book.mech=request.POST.get("mech")
                    book.civil=request.POST.get("civil")
                    book.ece=request.POST.get("ece")
                    book.eee=request.POST.get("eee")
                    book.chemical=request.POST.get("chemical")
                    book.cse=request.POST.get("cse")
                    book.save()
                    return render(request,'campus/comlog.html',{'s':s})


        else:
            x = request.user.username
            y = comp_details.objects.filter(username=x)
            y = str(y[0].company_name)
            y=y.split()
            y1=""
            for i in y:
                y1=y1+"_"+i
            y1=y1[1:len(y1)]

            return render(request, 'campus/jd.html', {'x':x,'y':y1})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")


def deletevacan(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        if request.method == "POST":
                    s=""
                    book=job_pos.objects.filter(job_id=request.POST.get("jobid"))
                    print(len(book))
                    if(len(book)!=1):
                        s="wrong job id try again"
                        return render(request, 'campus/jobdelete.html',{'s':s})
                    applied_jobs.objects.filter(job_id=book[0]).delete()
                    book[0].delete()
                    s="deleted succssefully"
                    return render(request,'campus/comlog.html',{'s':s})


        else:

            return render(request, 'campus/jobdelete.html')
    else:
        return HttpResponse("<h1>u r not logged in</h1>")

def viewpos(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        x = request.user.username
        y = job_pos.objects.filter(username=x)
        s=""
        print(y)
        if(len(y)==0):
            s="no vacancies posted"
        return render(request, 'campus/viewpos.html',{'y':y,'s':s})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")



def applyjob(request):
    if request.user.is_authenticated and request.user.groups.filter(name='student').exists() or request.user.is_superuser:
      s=""
      y=[]
      if request.method == "POST":
        print("hi")
        sal=request.POST.get("salary")
        bon=request.POST.get("years")
        x = request.user.username
        b = stu_details.objects.filter(username=x)
        b = str(b[0].branch)
        print(sal,bon,b)
        if(b.find("it") or b.find("information") or b.find("technology")):
         y = job_pos.objects.filter(salary__gte=sal,bond_years__lte=bon,information_technology="yes").order_by('salary')
        if ((b.find("cse")) or (b.find("computer"))):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,cse="yes").order_by('salary')
        if (b.find("me") or b.find("mechanical")):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,mech="yes").order_by('salary')
        if (b.find("ce") or b.find("civil")):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,civil="yes").order_by('salary')
        if (b.find("eee") or b.find("electrical")):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,eee="yes").order_by('salary')
        if (b.find("ece") or b.find("electronics")):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,ece="yes").order_by('salary')
        if (b.find("ch") or b.find("chemical")):
            y = job_pos.objects.filter(salary__gte=sal, bond_years__lte=bon,chemical="yes").order_by('salary')
        print(y)
        if(len(y)==0):
            s="no vacancies for this preference"
            print("failed",s)
            return render(request, 'campus/applyjob.html',{'s':s})
        else:
            return render(request, 'campus/applyjob.html', {'y': y, 's': s})
      else:
          return render(request, 'campus/applyjob.html', { 'y':y,'s': s})
    else:
        return HttpResponse("<h1>u r not logged in</h1>")


def apply(request,opt):
    if request.user.is_authenticated and request.user.groups.filter(name='student').exists() or request.user.is_superuser:
        if request.method=="POST":
            x=request.user.username
            print(x)
            y=job_pos.objects.filter(job_id=opt)[0].username
            job=applied_jobs()
            job.student_id=x
            job.company_id=y
            job.job_id=opt
            job.status="Applied!"
            job.save()
            return HttpResponse("<h1>you have applied succesfully... all the best</h1>")


        else:
            c=job_pos.objects.filter(job_id=opt)[0].username
            print(c)
            x=comp_details.objects.filter(username=c)
            print(x)
            return render(request,'campus/compdisp.html',{'post':x[0]})

    else:
        return HttpResponse("<h1>u r not logged in</h1>")


def selectstu(request):
    y=[]
    s=""
    statusForY = []
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        if request.method == "POST":
             jobid=request.POST.get("jobid")
             u=request.user.username
             x=len(job_pos.objects.filter(job_id=jobid,username=u))
             if(x==0):
                 s="Enter correct job id"
                 return render(request, 'campus/sstu.html', {'y': y,'s':s})
             x=len(applied_jobs.objects.filter(job_id=jobid,company_id=u))
             if(x==0):
                s = "sorry no one applied"
                return render(request, 'campus/sstu.html', {'y': y, 's': s})
             skillspreferred=request.POST.get("skillspreferred")

             x = applied_jobs.objects.filter(job_id=jobid,company_id=u).values('student_id')
             y=[]
             print(x)
             y=[]
             print("the total number is",len(y))
             for i in x:
                 b=stu_details.objects.filter(username=i['student_id'])
                 if(b.count()>0):
                     for candidate in b:
                         if(candidate.skills.find(skillspreferred)):
                             y.append(b)
             print("the total number is",len(y))
             if(len(y)==0):
                 s = "requirements not satisfied"
                 return render(request, 'campus/sstu.html', {'y': y, 's': s,'jobid':jobid})
             else:
                 print(y)
                 for i in y:
                     currentStudent=i[0]
                     iStatus=applied_jobs.objects.filter(job_id=jobid, student_id=currentStudent.username)
                     if (len(iStatus) > 0):
                         statusForY.append(iStatus[0].status)
                # statusForY.insert(0,' ')
                 print(statusForY)
                 reqdArr=[]
                 for i in range(0,len(y)):
                     reqdArr.append((y[i],statusForY[i]))
                 print(reqdArr)
                 return render(request, 'campus/sstu.html', {'y': y, 's': s,'jobid':jobid,'statusForY':statusForY,'reqdArr':reqdArr})


        else:
          return render(request, 'campus/sstu.html', {'y': y,'statusForY':statusForY})

    else:
        return HttpResponse("<h1>u r not logged in</h1>")


def stumail(request,jobid,opt):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        if request.method=="POST":
            recv=stu_details.objects.filter(username=opt)[0].email
            name=stu_details.objects.filter(username=opt)[0].name
            p=request.user.username
            p=comp_details.objects.filter(username=p)[0].company_name

            from_email = comp_details.objects.filter(username=request.user.username)[0].email

            print(recv,p)
            subject="Job Application-"+str(jobid)+" Update|| "+p
            body="Congratulations!!! "+str(name)+" Your application is selected for the further rounds in interview process,the date for the interview will be announced by your Placement Officer"

            if subject and body and from_email:
                try:
                    send_mail(subject, body, from_email, [recv])
                except BadHeaderError:
                    return HttpResponse('Invalid header found.')
                return redirect('/')
            else:
                return HttpResponse('Make sure all fields are entered and valid.')

            return HttpResponse("<h1>mail sent </h1>")


        else:
            appliedJob=applied_jobs.objects.filter(company_id=request.user.username,job_id=jobid,student_id=opt)[0]
            appliedJob.status="Selected For Next Round!"
            appliedJob.save()
            x=stu_details.objects.filter(username=opt)
            return render(request,'campus/showstudent.html',{'post':x[0]})

    else:
        return HttpResponse("<h1>u r not logged in</h1>")


def FilterCandidates(request):
    if request.user.is_authenticated and request.user.groups.filter(name='company').exists() or request.user.is_superuser:
        x = request.user.username
        y = job_pos.objects.filter(username=x)
        candidateList= Resume.Objects.filter(skills='')
        s = ""
        print(y)
        if (len(y) == 0):
            s = "no vacancies posted"
        return render(request, 'campus/viewpos.html', {'y': y, 's': s})
    #return render(request,'campus/FilterCandidate.html')
    else:
        return HttpResponse("<h1>u r not logged in</h1>")
