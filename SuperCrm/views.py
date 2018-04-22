# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse,redirect
from django.contrib.auth import authenticate,login,logout

# Create your views here
def Mylogin(request):
    # print models.Customer._meta.verbose_name
    # print request.POST

    # print next_url
    if request.user.is_authenticated():
        return redirect('/Myadmin/')
    next_url= request.GET.get('next','')
    if request.method=="POST":
        _user= request.POST.get('email')
        _passwd=request.POST.get('passwd')
        user = authenticate(username=_user, password=_passwd)
        if user :
        # the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                login(request,user)
                if next_url:
                    return redirect(next_url)
                else:
                    return redirect('/Myadmin/')
            else:
                print("The password is valid, but the account has been disabled!")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    return render(request, "login.html",locals())

def Mylogout(requesr):
    logout(requesr)
    return render(requesr, "login.html")