from django.shortcuts import render
from user_app.models import User
from user_app.forms import UserInfoForm,UserForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    return render(request,'user_app/index.html')

def out(request):
    return render(request,'user_app/logout.html')

@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('out'))

def register(request):
    reg = False
    if request.method == 'POST':
        user_info = UserForm(data=request.POST)
        profile_info = UserInfoForm(data=request.POST)
        
        if user_info.is_valid() and profile_info.is_valid():
            user = user_info.save()
            user.set_password(user.password)
            user.save()

            profile = profile_info.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            reg = True

        else:
            print(user_info.errors,profile_info.errors)
    else:
        user_info = UserForm()
        profile_info = UserInfoForm()

    return render (request,'user_app/reg.html',{'user_info':user_info,'profile_info':profile_info,'reg':reg})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)

        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'user_app/log.html', {})