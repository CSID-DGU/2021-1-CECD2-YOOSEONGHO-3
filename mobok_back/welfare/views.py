from django.shortcuts import render
from .serializers import WelfareSerializer
from .models import Welfare
import django_filters.rest_framework
from rest_framework import viewsets
from rest_framework.filters import SearchFilter

# Create your views here.
# views.py : 프론트앤드 혹은 서버에서 온 요청을 클래스와 함수를 통해 어떻게 응답할 것인가를 작성하는 파일

class WelfareView(viewsets.ModelViewSet):
    serializer_class=WelfareSerializer
    queryset=Welfare.objects.all()

    filter_backends = [SearchFilter]
    search_fields = ['domain']



    