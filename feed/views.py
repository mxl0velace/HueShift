from django.shortcuts import render
from .models import Post

# Create your views here.

def index(request):
    posts = Post.objects.order_by('-id')
    context = {'post_list' : posts}
    return render(request, 'feed/index.html', context)