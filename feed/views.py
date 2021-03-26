from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Vote
from django.http import HttpResponse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

# Create your views here.

def index(request):
    if request.method == 'GET':
        posts = Post.objects.order_by('-id')
        context = {'post_list' : posts}
        return render(request, 'feed/index.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            postid = int(request.POST['pid'])
            hue = int(request.POST['hue'])
            v = Vote.objects.get_or_create(author=request.user,post=Post(id=postid))[0]
            v.hue = hue
            v.save()
            return HttpResponse(Post(id=postid).hue)
        else:
            return HttpResponse(status=401)

@login_required
def makepiece(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            return redirect('/')
        else:
            print("Invalid post?")
    return render(request, 'feed/post.html', {'form':form})

def artist(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    posts = Post.objects.filter(author=user).order_by('-id')
    return render(request, 'feed/artist.html', {'post_list':posts, 'artist':user })