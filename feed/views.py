from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Vote
from django.http import HttpResponse
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db.models import Q

# Create your views here.

SEARCH_RANGE = 60
PER_PAGE = 20

def index(request):
    if request.method == 'GET':
        pagenum = handlePagenum(request)
        posts = Post.objects.order_by('-id')[(pagenum-1)*PER_PAGE:pagenum*PER_PAGE]
        context = {'post_list' : posts, 'pagenum':pagenum}
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
    pagenum = handlePagenum(request)
    posts = Post.objects.filter(author=user).order_by('-id')[(pagenum-1)*PER_PAGE:pagenum*PER_PAGE]
    return render(request, 'feed/artist.html', {'post_list':posts, 'artist':user, 'pagenum':pagenum})

def search(request):
    hue = int(request.GET.get("h",0))
    pagenum = handlePagenum(request)
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
    return render(request,'feed/search.html', {'post_list':posts[(pagenum-1)*PER_PAGE:pagenum*PER_PAGE], 'search_hue':hue, 'pagenum':pagenum})

def handlePagenum(request):
    pageN = request.GET.get('page',1)
    pagenum = 1
    try:
        pagenum = int(pageN)
        if pagenum < 1:
            pagenum = 1
    except ValueError:
        pagenum = 1
    return pagenum