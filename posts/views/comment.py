from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from posts.models import Comment
from posts.serializers import CommentSerializer

class CommentViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    