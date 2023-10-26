from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.generic import View

from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from .utils import generate_token

from django.utils.encoding import force_bytes,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import authenticate,login,logout
# Create your views here.
# Hàm đăng nhập
def signup(request):
    if request.method=="POST":
        username= request.POST['username']
        email=request.POST['email']
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if User.objects.filter(username=username).exists():
            messages.warning(request,"This username already exists")
            return render(request,'login.html') 
        if User.objects.filter(email=email).exists():
            messages.warning(request,"This email already exists")
            return render(request,'login.html') 
        if password!=confirm_password:
            messages.warning(request,"The two passwords do not match")
            return render(request,'login.html')                   
        user = User.objects.create_user(username,email,password)
        user.first_name = "Member #" + str(user.id)
        user.is_active=False
        user.userprofile = UserProfile()
        user.userprofile.save()
        user.save()
        # send email to activate 
        email_subject="Activate Your Account"
        message=render_to_string('activate.html',{
            'user':user,
            'domain':'127.0.0.1:8000',
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
        email_message.send()
        messages.success(request,"Activate Your Account by clicking the link in your gmail")
        return redirect('/auth/login/')
    return render(request,"login.html")

def handlelogin(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        myuser=authenticate(username=username,password=password)

        if myuser is not None:
            login(request,myuser)
            messages.success(request,"Login Success")
            return redirect('/')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/auth/login')

    return render(request,'login.html')

def handlelogout(request):
    logout(request)
    messages.info(request,"Logout Success")
    return redirect('/auth/login')

def handleprofile(request):
    return render(request,'my-profile.html')

def changeProfile(request):
    if not request.user.is_authenticated:
        messages.warning(request,"You need to log in to access")
        return redirect('/auth/login')
    if request.method == "POST":
        current_user = request.user
        user = User.objects.get(id=current_user.id)
        user.first_name = request.POST.get('first_name')
        user.userprofile.phone = request.POST.get('phone')
        oldpass = request.POST.get('oldpass')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        try:
            if request.POST.get('changepass') != None:
                if not check_password(oldpass, user.password):
                    messages.warning(request,"Incorrect Password")
                    return redirect('/auth/profile')
                if pass1 == pass2:
                    user.set_password(pass1)
                    user.save()
                else:
                    messages.warning(request,"Password not same")
                    return redirect('/auth/profile')
            if len(request.FILES) != 0:
                user.userprofile.avatar = request.FILES['avatar']
            user.userprofile.save()
            user.save() 
            messages.success(request,"You have updated succes")
            return redirect('/auth/login')
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'status': 'error', 'message': 'Order detail error'})

class ActivateAccountView(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user,token):
            user.is_active=True
            user.save()
            messages.success(request,"Account Activated Successfully")
            return redirect('/auth/login')
        messages.warning(request,"You have already activated your account")
        return render(request,'login.html')
    
class RequestResetEmailView(View):
    def post(self,request):
        email=request.POST['email']
        users=User.objects.filter(email=email)
        if users.exists():
            user = users.first()  # Lấy người dùng đầu tiên trong danh sách
            email_subject='[Reset Your Password]'
            message=render_to_string('reset-user-password.html',{
                'domain':'127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':PasswordResetTokenGenerator().make_token(user)
            })

            email_message = EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email])
            email_message.send()

            messages.success(request,"Check your email to reset your password")
            return render(request,'login.html')
        else:
            messages.warning(request,"Email address is not correct. Please try again")
            return render(request,'login.html')

class SetNewPasswordView(View):
    def get(self,request,uidb64,token):
        context = {
            'uidb64' : uidb64,
            'token' : token
        }
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.warning(request,"The link is no longer valid")
                return render(request,'login.html')
        except DjangoUnicodeDecodeError as identifier:
            pass
        messages.success(request,"Please enter your password to reset your account password")
        return render(request,'set-new-password.html',context)

    def post(self,request,uidb64,token):
        context={
            'uidb64':uidb64,
            'token':token
        }
        password=request.POST['pass1']
        confirm_password=request.POST['pass2']
        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'set-new-password.html',context)
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request,"Password reset successfully, please log in again with new password")
            return redirect('/auth/login/')
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request,'set-new-password.html',context)

