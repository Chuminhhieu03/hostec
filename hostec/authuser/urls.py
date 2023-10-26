from django.urls import path
from authuser import views

urlpatterns = [
    path('signup/',views.signup,name="signup"),
    path('login/',views.handlelogin,name="handlelogin"),
    path('logout/',views.handlelogout,name="handlelogout"),
    path('profile/',views.handleprofile,name="handleprofile"),
    path('changeprofile/',views.changeProfile,name="changeProfile"),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
    path('reset/<uidb64>/<token>',views.SetNewPasswordView.as_view(),name='reset'),
    path('request-reset-email/',views.RequestResetEmailView.as_view(),name='request-reset-email'),
]