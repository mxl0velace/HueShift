from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Vote
from django.http import HttpResponse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.

SEARCH_RANGE = 60

def index(request):
    if request.method == 'GET':
        posts = Post.objects.order_by('-id')
        context = {'post_list' : posts}
        return render(request, 'feed/index.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            postid = int(request.POST['pid'])
            if request.POST['action'] == 'shift':
                hue = int(request.POST['hue'])
                post = Post.objects.get(id=postid)
                vlist = Vote.objects.filter(author=request.user,post=post)
                if len(vlist) != 0:
                    v = vlist[0]
                    v.hue = hue
                    v.save()
                else:
                    v = Vote(author=request.user, post=post, hue=hue)
                    v.save()
                return HttpResponse(Post.objects.get(id=postid).hue) # Updated colour
            elif request.POST['action'] == 'delete':
                p = Post.objects.get(id=postid)
                if p.author == request.user:
                    p.delete()
                    return HttpResponse(status=204) # Accepted
                else:
                    return HttpResponse(status=401) # Unauthorised
            else:
                return HttpResponse(status=400) # Bad Request
        else:
            return HttpResponse(status=401) # Unauthorised

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

def search(request):
    hue = int(request.GET.get("h",0))
    lowerbound = hue - (SEARCH_RANGE / 2)
    upperbound = hue + (SEARCH_RANGE / 2)
    posts = Post.objects.none()
    if lowerbound < 0:
        posts = posts | Post.objects.filter(hue__range=(0,hue)) | Post.objects.filter(hue__gte=360+lowerbound)
    else:
        posts = posts | Post.objects.filter(hue__range=(lowerbound,hue))
    if upperbound > 360:
        posts = posts | Post.objects.filter(hue__range=(hue,360)) | Post.objects.filter(hue__lte=upperbound-360)
    else:
        posts = posts | Post.objects.filter(hue__range=(hue,upperbound))
    return render(request,'feed/search.html', {'post_list':posts, 'search_hue':hue})