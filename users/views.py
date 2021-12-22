from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
import re
# Create your views here.

def user_login(request):
    if request.method == 'POST':  # check if the request is POST request and it contains any parameter
        # take the data from username field and put it in a variable
        email = request.POST['email']
        # take the data from username field and put it in a variable
        password = request.POST['password']
        user = authenticate(request, email=email,
                            password=password)  # authenticates the user
        if user is not None:  # check if the user is inside our database
            # login the user if they are authenticated properly
            login(request, user)
            # save user's id and email into session
            request.session['user_id'] = user.id
            request.session['user_email'] = user.email
            # after successful login return them into HomePage
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('dashboard')
                # return render(request, 'dashboard/dashboard.html')
        else:
            print("In Else")
            # If the username or password is not
            messages.error(request, 'Your username or password is invalid.')
            # matching then give a message
    # categories = Category.objects.all()

    # context = {'categories': categories,
    #            }
    return render(request, 'login/login.html')

# simple logout function
def user_logout(request):
    logout(request)  # normal logout function
    return redirect('/')

# user password change
@login_required(login_url='user/login/')
def user_password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated')
            return redirect('dashboard')
        else:
            error_message = str(form.errors)
            print("ERRROR" , error_message)
            error_message = error_message.replace("old_password" , "")
            error_message = error_message.replace("new_password2" , "")
            error_message = error_message.replace("new_password1" , "")
            clean = re.compile('<.*?>')
            text = re.sub(clean, '', error_message)
            print(text.replace("." , "<br>"))
            messages.error(request, error_message)
            
            return redirect('user_password_change')
    form = PasswordChangeForm(request.user)
    context = {
        "form" : form
    }
    return render(request, 'login/pass-change.html', context)