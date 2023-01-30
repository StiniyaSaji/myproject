import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect

from newproject.form import RegisterForm, UserBlogForm, UserImageForm
import requests

from newproject.models import UserBlog, Profile

def UserRegister(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(Userlogin)
    return render(request,'reg.html',{'form':form})

def Userlogin(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            print(request.user.username)
            return redirect(ViewBlog)
        else:
            return redirect(Userlogin)
            return HttpResponse('Invalid username or password')
    return render(request,'login.html')

def Userlogout(request):
    logout(request)
    return redirect(Userlogin)

def ForgotPassword(request):
    if request.method == "POST":
        phone = request.POST['phone']
        userdata = Profile.objects.get(phone=phone)
        if userdata:
            url = 'https://2factor.in/API/V1/b866434b-7c4c-11ed-9158-0200cd936042/SMS/{}/AUTOGEN'.format(str(phone))

            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.request("GET", url, headers=headers, data=payload)
            data = response.json()

            r = data['Details']
            request.session['Details'] = r
            request.session['phone'] = phone

            if data['Status'] == 'Success':
                return redirect(ResetPassword)
        else:
            return  redirect(ForgotPassword)

    return render(request,'forgotpass.html')

def ResetPassword(request):
    if request.method == "POST":
        otp = request.POST['OTP']
        passwd = request.POST['newpass']
        cpasswd = request.POST['confirmpass']
        details = request.session.get('Details')
        api = 'https://2factor.in/API/V1/b866434b-7c4c-11ed-9158-0200cd936042/SMS/VERIFY3/{}/{}'.format(details, otp)
        res = requests.get(api).json()
        print(res)
        phone = request.session.get('phone')

        if res['Status'] == 'Success':
            if passwd == cpasswd:
                userdata = Profile.objects.get(phone=phone)
                data = User.objects.get(id=userdata.user_id)
                u = User.objects.get(username = data.username)
                u.set_password(passwd)
                u.save()

                return redirect(Userlogin)
    return render(request, 'resetpass.html')

# def image_request(request):
#     form = UserImageForm()
#     if request.method == 'POST':
#         form = UserImageForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             img_object = form.instance
#             return render(request, 'createblog.html', {'form': form, 'img_obj': img_object})
#     return render(request, 'createblog.html', {'form': form})

def upload_image(request):
    if request.method == "POST" and request.FILES['images']:
        upload = request.FILES['images']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)
        Profile.objects.filter(user_id=request.user.id).update(profile_pic=file_url)
        return redirect(ViewProfile)
    return render(request,'propic.html')

def ViewBlog(request):
    vlog = UserBlog.objects.all()
    return render(request,'viewblog.html',{'vlog':vlog})

def CreateBlog(request):
    form = UserBlogForm()
    if request.method == "POST":
        topic = request.POST['topic']
        title = request.POST['title']
        blogcontent = request.POST['content']

        obj = UserBlog.objects.create(user_id_id=request.user.id,topic=topic,caption=title,blog_data=blogcontent,created_date=datetime.datetime.now())
        obj.save()
        form = UserBlogForm(request.FILES)
        if form.is_valid():
            form.save()

            return redirect(ViewBlog)
    return render(request, "createblog.html",{"form":form})

def DeleteBlog(request,id):
    datas = UserBlog.objects.get(id=id)
    datas.delete()
    return redirect(ViewBlog)

def UpdateBlog(request,id):
    data = UserBlog.objects.get(id=id)
    if request.method == "POST":
        topic = request.POST['topc']
        title = request.POST['title']
        blogcontent = request.POST['content']

        upload = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save(upload.name, upload)
        file_url = fss.url(file)

        UserBlog.objects.filter(id=id).update(topic=topic, caption=title, blog_data=blogcontent,
                                image=file_url,updated_date=datetime.datetime.now())
        return redirect(ViewBlog)
    return render(request, 'updateblog.html', {'i':data})

def CreateProfile(request):
    data = User.objects.get(id = request.user.id)
    if request.method == "POST":
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['addr']
        city = request.POST['city']
        prof = Profile.objects.create(user_id=request.user.id,phone=phone,DOB=dob,address=address,city=city )
        prof.save()
        return redirect(CreateBlog)
    return render(request, "createprofile.html", {'data': data})

def ViewProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    date_join = data.date_joined
    return render(request, 'viewprofile.html', {'data':data,'data1':data1,'date_join':date_join.date()})

def EditProfile(request):
    current_user = request.user
    data = User.objects.get(id=current_user.id)
    data1 = Profile.objects.get(user_id=current_user.id)
    if request.method == "POST":
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        phone = request.POST['phone']
        dob = request.POST['dob']
        address = request.POST['addr']
        city = request.POST['city']

        User.objects.filter(id=current_user.id).update(first_name=first_name,last_name=last_name,email=email)
        Profile.objects.filter(user_id=request.user.id, phone=phone, DOB=dob, address=address, city=city)
        return redirect(ViewProfile)
    return render(request, 'editprofile.html', {'data': data,'data1':data1})
