from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from django.contrib.auth import authenticate, login

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Account of " + request.user.username)

def signup(request):
    if request.user.is_authenticated:
        return index(request)
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request,user)
                return redirect('/')
            else:
                print("Signup Failed")
        else:
            form = SignUpForm()
        return render(request, 'account/signup.html', {'form': form})