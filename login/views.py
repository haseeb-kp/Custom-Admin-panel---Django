
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import login,logout
from django.views.decorators.cache import never_cache
from django.db.models import Q


# Create your views here.
@never_cache
def index(request):
    return redirect('user_login')

@never_cache
def user_login(request):
    if request.user.is_superuser :
        return redirect('admin_dashboard')
    if 'username' in request.session:
        return redirect('home')
    if request.method=='GET':
        return render(request,'user_login.html')
    if request.method == 'POST':            
        username =request.POST['username']
        password =request.POST['password']

        user=auth.authenticate(username=username,password=password)

        if user is not None:
            # login(request, user)
            # auth.login(request, user)
            request.session['username']=username
            return redirect('home')   
        else:
            messages.error(request, 'Wrong credentials!!!')
            return redirect('index')
@never_cache
def signup(request):
    if request.method=='GET':
        return render(request,'signup.html')

    if request.method=='POST':
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        phonenumber= request.POST['phone_number']
        # dob = request.POST['dob']
        email= request.POST['email']
        user_name= request.POST['user_name']
        pass1= request.POST['pass1']
        pass2= request.POST['pass2']
        
        if pass1==pass2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'email taken')
                return redirect('signup')
             
            elif User.objects.filter(username=user_name).exists():
                messages.error(request, 'Username taken')
                return redirect('signup')  
            else:
                user= User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=pass2,phonenumber=phonenumber)
                user.save()
                return redirect('user_login')
            

            
        else:
            messages.error(request, 'Password not matching')
            return redirect('signup')

    
@never_cache
def home(request):
    if 'username' in request.session:
        user = User.objects.all()
        return render(request,'home.html',{'user':user}) #
    return redirect('index')
    

def user_logout(request):
    if 'username' in request.session:
        request.session.flush()
        # logout(request)
    return redirect('index')

@never_cache
def admin_login (request):
    if request.user.is_superuser :
        return redirect('admin_dashboard')
    if request.method=='GET':
        return render(request,'admin_login.html')
    if request.method == 'POST':            
        username =request.POST['s_username']
        password =request.POST['s_password']
        user=auth.authenticate(username=username,password=password)
        
        if user is not None and user.is_superuser:
            login(request, user)           #authenticates //creates session
            # request.session['username']= username
            return redirect('admin_dashboard')   
        else:
            messages.error(request, 'Wrong credentials!!!')
            return redirect('admin_login')

@never_cache
def admin_dashboard(request):
    if request.user.is_authenticated and  request.user.is_superuser :
        if 'search' in request.GET:
            search = request.GET['search']
            multiple_search = Q(Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(username__icontains=search))
            user_list = User.objects.filter(multiple_search)
        else:
            user_list = User.objects.all()
        return render(request,'admin_dashboard.html',{'user_list':user_list})
    else: 
        return redirect('admin_login')

def admin_logout(request):
    if request.user.is_superuser:
        logout(request)
    return redirect('admin_login')

@never_cache
def add_user(request):
    if request.user.is_superuser:
        if request.method=='GET':
            return render(request,'add_user.html')

        if request.method=='POST':
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            # phone_number= request.POST['phone_number']
            # dob = request.POST['dob']
            email= request.POST['email']
            user_name= request.POST['user_name']
            pass1= request.POST['pass1']
            pass2= request.POST['pass2']
            
            if pass1==pass2:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email taken')
                    return redirect('add_user')
                
                elif User.objects.filter(username=user_name).exists():
                    messages.error(request, 'Username taken')
                    return redirect('add_user')  
                else:
                    user= User.objects.create_user(username=user_name,first_name=first_name,last_name=last_name,email=email,password=pass2)
                    user.save()
                    return redirect('admin_dashboard')   
            else:
                messages.error(request, 'Password not matching')
                return redirect('add_user')
    else:
        return redirect('admin_dashboard')


@never_cache
def edit_user(request,id):
    if request.user.is_superuser:
    
        newUser = User.objects.get(id=id)
        
        if request.method=='POST':
            
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            email= request.POST['email']
            user_name= request.POST['user_name']

        
            newUser.first_name = first_name
            newUser.last_name = last_name
            newUser.user_name = user_name
            newUser.email = email
            newUser.save()
            return redirect('admin_dashboard')

        return render(request,'edit_user.html',{'newUser':newUser})
    else:
        return redirect('admin_login')

def delete_user(request,id):
    user = User.objects.get(id=id)
    user.delete()
    return redirect('admin_dashboard')
