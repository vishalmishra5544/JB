from django.shortcuts import render, redirect
from pyresparser import ResumeParser
from .models import Resume
from .forms import UploadResumeModelForm
from django.contrib import messages
from django.conf import settings
from django.db import IntegrityError
from django.http import HttpResponse, FileResponse, Http404
from campus.models import stu_details
import os


def homepage(request):
    if request.method == 'POST':
        file_form = UploadResumeModelForm(request.POST, request.FILES)
        files = request.FILES.get('resume',False)
        print(files,"-----------------")
        resumes_data = []
        file=files
        print(file,"------------------")
        reqdname=""
        if file_form.is_valid():
                try:
                    # saving the file

                    resume = Resume(resume=file)
                    resume.save()

                    # extracting resume entities
                    parser = ResumeParser(os.path.join(settings.MEDIA_ROOT, resume.resume.name))
                    data = parser.get_extracted_data()
                    print(data)
                    resumes_data.append(data)
                    resume.name = data.get('name')
                    reqdname=resume.name
                    previousresumes = Resume.objects.filter(name=reqdname)
                    previousresumes.delete()
                    resume.email = data.get('email')
                    resume.mobile_number = data.get('mobile_number')
                    if data.get('degree') is not None:
                        resume.education = ', '.join(data.get('degree'))
                    else:
                        resume.education = None
                    #resume.company_names = data.get('company_names')
                    #resume.college_name = data.get('college_name')
                    resume.designation = data.get('designation')
                    #resume.total_experience = data.get('total_experience')
                    if data.get('skills') is not None:
                        resume.skills = ', '.join(data.get('skills'))
                    else:
                        resume.skills = None
                    if data.get('experience') is not None:
                        resume.experience = ', '.join(data.get('experience'))
                    else:
                        resume.experience = None
                    resume.save()
                except IntegrityError:
                    messages.warning(request, 'Duplicate resume found:', file.name)
                    return redirect('homepage')
                resumes = Resume.objects.filter(name=reqdname)
                context = {
                    'resumes': resumes,
                }
                stu = request.user.username
                skillsreqd = ""
                if(stu_details.objects.filter(username=stu).count()<=0):
                    studentDetails = stu_details(username=stu,name=resume.name,phone_number=resume.mobile_number,email=resume.email,branch=resume.education,skills=skillsreqd.join(resume.skills),experience=resume.experience)
                    studentDetails.save()
                else:
                    student=stu_details.objects.filter(username=stu)[0]
                    student.phone_number=resume.mobile_number
                    student.email=resume.email
                    student.branch=resume.education
                    student.skills=skillsreqd.join(resume.skills)
                    student.experience=resume.experience
                    student.save()
                messages.success(request, 'Resumes uploaded!')
                return render(request, 'base.html', context)
    else:
        form = UploadResumeModelForm()
    return render(request, 'base.html', {'form': form})
