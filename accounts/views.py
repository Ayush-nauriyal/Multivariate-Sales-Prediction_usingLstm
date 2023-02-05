from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.shortcuts import redirect, render
from django.contrib.auth import logout,login, authenticate


# Create your views here.
def logout(request):
        auth.logout(request)
        return redirect('/')

def login(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,' invalid credentials')
            return redirect('login')

    else:
        return render(request,'login.html')


def register(request):
    if request.method == 'POST':
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        user=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['password1']
        pass2=request.POST['password2']

        if pass2==pass1:
            if User.objects.filter(username=user).exists():
                messages.info(request,'Username already taken please try another username')
                return redirect('register')
            elif  User.objects.filter(email=email).exists():
                messages.info(request,'email already taken please try another email') 
                return redirect('register')  
            else:    
                user=User.objects.create_user(username=user,password=pass1,email=email,first_name=first_name,last_name=last_name)
                user.save()
                return redirect('login')

        else:
            messages.info(request,'you entered passwords dont match each other please fill carefully')
            return redirect('register')

    else:
       return render(request,'register.html')