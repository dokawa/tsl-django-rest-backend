from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response

from wall_app.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
    	super().post(request).data
    	return Response({"success":True},status=201)

