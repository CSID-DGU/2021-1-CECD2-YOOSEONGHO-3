from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import UserLoginSerializer
from .serializers import UserCreateSerializer
from .models import User


#permission_classes([AllowAny])의 역할에 대해 정리하면,
#처음에 settings에서 rest framework설정 중 permission에 대해 인증된 경우만
#가능하도록 했었다. 그래서 이 함수는 인증이 없어도 접근 가능하게 만든 것.,

@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)
 


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)
        
        print(serializer.data)
        response = {
            'success': 'True',
            'username':serializer.data['username'],
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)