from django.shortcuts import render
from .models import Post, Vote
from django.http import HttpResponse

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
            existing = Vote.objects.filter(id=postid,author=request.user)
            if len(existing) == 0:
                p = Post(id=postid)
                Vote(author=request.user,post=p,hue=hue).save()
            else:
                existing[0].hue = hue
                existing[0].save()
            return HttpResponse(status=201)