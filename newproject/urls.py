from django.urls import path

from newproject import views

urlpatterns = [
    path('',views.Userlogin),
    path('register',views.UserRegister),
    path('logout',views.Userlogout),
    path('login',views.Userlogin),
    path('verify',views.ForgotPassword),
    path('reset',views.ResetPassword),
    # path('imag',views.image_request),
    path('create',views.CreateBlog),
    path('view', views.ViewBlog),
    path('delete/<int:id>',views.DeleteBlog),
    path('update/<int:id>',views.UpdateBlog),
    path('createpro',views.CreateProfile),
    path('viewpro', views.ViewProfile),

]