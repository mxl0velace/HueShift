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
            v = Vote.objects.get_or_create(author=request.user,post=Post(id=postid))[0]
            v.hue = hue
            v.save()
            return HttpResponse(Post(id=postid).hue)
        else:
            return HttpResponse(status=401)