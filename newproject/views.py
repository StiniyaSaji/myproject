from django.contrib.auth import authenticate, login, logout
from django.contrib.sites import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader, context

from newproject import form
from newproject.form import RegisterForm, UserBlogForm, UserImageForm
import requests

from newproject.models import UserBlog


def data(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(userlogin)
    return render(request,'home.html',{'form':form})

def UserRegister(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(userlogin)
    return render(request,'reg.html',{'form':form})

def userlogin(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print(request.user.username)
            return redirect(ViewBlog)
        else:
            return redirect(userlogin)
            return HttpResponse('Invalid username or password')
    return render(request,'login.html')

def userlogout(request):
    logout(request)
    return redirect(userlogin)

def VerifyOTP(request):
    if request.method == "POST":
        phone = request.POST['phone']
        url = f'https://2factor.in/API/V1/b866434b-7c4c-11ed-9158-0200cd936042/SMS/+91{str(phone)}/AUTOGEN/OTP1'

        payload = {}
        headers = {}
        response = requests.request('GET', url, headers=headers, data=payload)
        res = response.json()
        if res['Status'] == 'Success':
            return redirect(ResetPassword)
        else:
            return HttpResponse('The mobile number you entered is incorrect')

    return render(request,'verifyotp.html')

def ResetPassword(request):
    if request.method == "POST":
        otp = request.POST['OTP']
        url = 'https://2factor.in/API/V1/b866434b-7c4c-11ed-9158-0200cd936042/SMS/VERIFY3/91(otp)'.format(otp)

        payload = {}
        headers = {}
        response = requests.request('GET', url, headers=headers, data=payload)
        res = response.json()
        if res['Status'] == 'Success':
            return redirect(userlogin)
        else:
            return HttpResponse('verification failed')

    return render(request, 'resetpass.html')

def ViewBlog(request):
    vlog = UserBlog.objects.all()
    return render(request,'viewblog.html',{'vlog':vlog})

# def images(request):
#   template = loader.get_template('createblog.html')
#
#   return HttpResponse(template.render(context, request))

def image_request(request):
    form = UserImageForm()
    if request.method == 'POST':
        form = UserImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            img_object = form.instance
            return render(request, 'createblog.html', {'form': form, 'img_obj': img_object})
    return render(request, 'createblog.html', {'form': form})

def CreateBlog(request):
    if request.method == "POST":
        topic = request.POST['topic']
        title = request.POST['title']
        blog_content = request.POST['content']
        obj = UserBlog.objects.create(topic=topic,caption=title,blog_data=blog_content)
        obj.save()
        return redirect('ViewBlog')
    return render(request, "createblog.html", {'obj': object})

def Delete(request,id):
    datas = UserBlog.objects.get(id=id)
    datas.delete()
    return redirect(ViewBlog)

def update(request,id):
    datas = UserBlog.objects.get(id=id)
    datas.topic = request.POST['topc']
    datas.caption = request.POST['title']
    datas.blog_data = request.POST['content']
    datas.save()
    return render(request, 'update.html',{'datas':datas})

def UserProfile(request):
    if request.method == "POST":
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['addr']
        city = request.POST['city']
        obj = UserBlog.objects.create(firstname=firstname,lastname=lastname,email=email,phone=phone,DOB=dob,address=address,
                                      city=city)
        obj.save()
    return render(request, "userprofile.html", {'obj': object})



