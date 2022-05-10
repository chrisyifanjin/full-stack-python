from django.views.generic.list import ListView
from requests import Response
from posts.models import Post
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from .models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view 
from rest_framework.response import Response
from rest_framework import status

class PostList(ListView):
    model = Post


class PostCreate(CreateView):
    model = Post 
    fields = ['image', 'title', 'author']
    success_url ='/'




class PostDetail(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(
            *args, **kwargs
        )
        return context

@api_view(['GET','POST'])
def post_list(request, format = None):

    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return JsonResponse({'posts': serializer.data})
    if request.method == 'POST':
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)

@api_view(['GET','PUT', 'DELETE'])
def post_detail(request, id, format = None):
    try: 
        post = Post.objects.get(pk = id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
