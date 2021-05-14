from rest_framework import serializers
from .models import Welfare

#Serializer란 직렬화하는 것으로, db 데이터를 사용하기 쉬운 json/Dictionary 형태로 변환하는 작업을 하는 것

class WelfareSerializer(serializers.ModelSerializer):
    class Meta:
        model=Welfare
        fields=('domain','title','description','link')
    