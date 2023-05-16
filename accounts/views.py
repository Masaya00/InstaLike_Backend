from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    print('通過')
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        print(request.__dict__)
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(name=name, email=email, password=password)
                return Response(
                    {'success': 'ユーザーの作成に成功しました'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'error': '既に登録されているメールアドレスです'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            print(e)
            return Response(
                {'error':'アカウント登録時に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UserView(APIView):
    def get(self, request):
        try:
            user = request.user
            user = UserSerializer(user, context={'request': request})

            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {'error': 'ユーザーの取得に問題が発生しました'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
