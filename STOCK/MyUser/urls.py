from django.urls import path
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('login/',views.login_view,name='login_view'),
    path('logout/',views.logout_view,name='logout_view'),
    path('qrcode/<int:pk>/',views.qrcode_view,name='qrcode'),
    path('register/',views.Register.as_view(), name='register'),
    path('confirmEmail/<uidb64>/<token>',views.LoginConfirm.as_view(), name='login_confirm'),
    path('facebook/',views.facebook_view, name='facebook'),
    path('google/',views.Google_view, name='google'),
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name="auth/password_reset.html",email_template_name="auth/password_reset_email.txt",html_email_template_name="auth/password_reset_email.html"), name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name="auth/password_reset_done.html"), name='password_reset_done'),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view( template_name="auth/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view( template_name="auth/password_reset_complete.html"), name="password_reset_complete"),
    #path('register/num/<str:user>/',views.registerNum_view, name='registerNum')
]