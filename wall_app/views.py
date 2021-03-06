from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework import permissions

from wall_app.models import WallPost
from wall_app.serializers import UserSerializer, WallPostSerializer, UserCreateSerializer, AnonymousUserCreateSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.core import mail


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'wall_posts': reverse('wall-post-list', request=request, format=format)
    })


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]


class WallPostViewSet(viewsets.ModelViewSet):
    queryset = WallPost.objects.all().order_by('-created')
    serializer_class = WallPostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserCreate(generics.CreateAPIView):
    serializer_class = UserCreateSerializer

    def post(self, request):
        super().post(request).data
        send_welcome_mail(request.data['email'])
        return send_welcome_mail(request.data['email'])


class AnonymousUserCreate(generics.CreateAPIView):
    serializer_class = AnonymousUserCreateSerializer

    def post(self, request):
        super().post(request).data
        return send_welcome_mail(request.data['email'])


def send_welcome_mail(email):
    try:
        mail.send_mail(
            'Welcome to Wall App',
            'Welcome to Wall App.\nTo start using, just post a mesage!',
            'tsl@gmail.com',
            [email],
            fail_silently=False,
        )
        return Response({"success": True}, status=201)
    except:
        return Response({"success": False}, status=420)
