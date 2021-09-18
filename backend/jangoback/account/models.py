from django.db import models

# Create your models here.
class Account(models.Model):
    #사용자 아이디와 패스워드
    userId=models.CharField(max_length=30, unique=True)
    password=models.CharField(max_length=30)
    
    #사용자가 입력한 나이로 청소년, 청년, 중장년, 노인 등으로 분류
    ageGroup=models.CharField(max_length=10)
    
    #이름
    name=models.CharField(max_length=20)
    
    #거주지역 정보
    area=models.CharField(max_length=20)
    detailArea=models.CharField(max_length=20)
    
    #사용자가 클릭했던 복지정보(추천을 위해 사용되는 필드)
    userClicked=models.TextField(null=True)
