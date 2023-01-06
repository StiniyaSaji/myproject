from django.urls import path

from newproject import views

urlpatterns = [
    path('',views.userlogin),
    path('register',views.UserRegister),
    path('logout',views.userlogout),
    path('login',views.userlogin),
    path('verify',views.VerifyOTP),
    path('reset',views.ResetPassword),
    path('myblog',views.MyBlog),
    # path('images',views.images),
    path('upload',views.image_request),
    path('create',views.Create),
    path('delete/<int:id>',views.Delete),
    path('update/<int:id>',views.update),

]