from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from posts.models import Post
from posts.serializers import PostSerializer

class PostViewset(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
