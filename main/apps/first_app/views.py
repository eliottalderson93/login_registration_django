from django.shortcuts import render, HttpResponse, redirect
from time import gmtime, strftime
from datetime import date, datetime
from .models import users
from django.contrib import messages
import bcrypt

def index(request):
    if 'initial' in request.session:
        request.session['initial'] = False
        if request.session['user_id'] != -1: #user is here
            messages.set_level(request,0) #otherwise will ignore add message
            messages.add_messages(request,0,'you are logged in')
            return redirect('/show/'+str(request.session['user_id'])) #keeps them logged in
        #print(request.session)
    else:
        request.session['initial'] = True #initialize
        request.session['user_id'] = -1
        request.session['create'] = False #turns true on successful registration
    if request.session['initial'] == False:
        pass
    return render(request, "django_app/code.html")

def login_page(request):
    return render(request,"django_app/login.html")

def login(request):
    if request.method == 'POST':
        errors = users.objects.login_validator(request.POST)
        category = 0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1               
                print(key,value,category)
                messages.set_level(request,category) #otherwise will ignore add message
                messages.add_message(request, category, value)    
            print('ERROR',errors,messages.storage.base)
            return redirect('/users/login_page')
        else: #no errors passed credentials true
            userID = users.objects.get(email = request.POST['email']).id
            return redirect("/users/"+str(userID))            
    else:
        return redirect('/users/login_page')
        
def create(request): #user registration
    if request.method == "POST":
        errors = users.objects.user_validator(request.POST)
        category=0
        key_prev = 'j'
        if len(errors):
            for key,value in errors.items():
                messages.set_level(request,category) #otherwise will ignore add message
                if key_prev != key: #allows for multiple errors to display over one box
                    key_prev = key
                    category += 1
                print(key,value,category)
                messages.add_message(request, category, value)    
            print('ERROR',errors,messages.storage.base)
            return redirect('/')
        else: #create user
            hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = users.objects.create(fname = request.POST['first_name'], lname = request.POST['last_name'], email = request.POST['email'], pw_hash = hash_pw)
            user_id = user.id
            request.session['create'] = True
            request.session['user_id'] = user_id
            print('CREATED::', user)
            return redirect("/users/"+str(user_id))
    else:
        return redirect('/')

def show(request, id): #success page
    if request.session['user_id'] != -1: #user is here
        this_user = users.objects.get(id = str(id))
        print('SHOW::',this_user)
        context = {'ID' : this_user.id,
                    'full_name' : (this_user.fname + ' ' + this_user.lname),
                    'email' : this_user.email,
                    'created_at' : this_user.created_at}
        request.session['first_name'] = this_user.fname
        return render(request,"django_app/user.html", context)
    else:
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/users')

# def edit(request, id):
#     this_user = users.objects.get(id = str(id))
#     print('EDIT::',this_user)
#     context = {'ID' : this_user.id,
#                 'fname' : this_user.fname,
#                 'lname' : this_user.lname,
#                 'email' : this_user.email,
#                 'created_at' : this_user.created_at}
#     return render(request, "django_app\edit_user.html", context)

# def destroy(request, id):
#     this_user = users.objects.get(id = str(id))
#     print('DESTROY::',this_user)
#     this_user.delete()
#     return redirect('/users')

# def update(request,id):
#     if request.method == "POST":
#         errors = users.objects.basic_validator(request.POST)
#         if len(errors):
#             for error in errors:
#                 messages.add_message(request, messages.INFO, error)
#         else:
#             this_user = users.objects.get(id = str(id))
#             this_user.fname = request.POST['first_name']
#             this_user.lname = request.POST['last_name']
#             this_user.email = request.POST['email']
#         return redirect(("/users/"+id))
#     else:
#         return redirect(("/users/"+id))
