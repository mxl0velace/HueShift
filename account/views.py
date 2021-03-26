from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# Create your views here.
@login_required
def index(request):
    return HttpResponse("Account of " + request.user.username)

def signup(request):
    if request.user.is_authenticated:
        return index(request)
    else:
        return render(request, 'account/signup.html', {'form': SignUpForm()})