from django.shortcuts import render

# Create your views here.
# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
import json
import django
from django.db import IntegrityError
django.setup()

from account.models import Account

# Create your views here.
def signup(request):
    data=json.loads(request.body)
    userId, password = data['userId'], data['password']
    name, age = data['name'], int(data['age'])
    area, detailArea = data['area'], data['detailArea']

    ageGroup=''
    #age값에 따른 연령대 결정
    if age<20:
        ageGroup='청소년'
    elif age<35:
        ageGroup='청년'
    elif age<65:
        ageGroup='중장년'
    else:
        ageGroup='노년'

    try:
        Account.objects.create(
            userId=userId,
            password=password,
            ageGroup=ageGroup,
            name=name,
            area=area,
            detailArea=detailArea
        )
    except IntegrityError as e:
        print('에러타입:', e, type(e))
        if 'UNIQUE constraint failed' in e.args[0]:
            return JsonResponse({'success':False,'type':'alreadyExists'}) 
        return JsonResponse({'success':False})

    return JsonResponse({'success':True})


def signin(request):
    data=json.loads(request.body)
    userId, password = data['userId'], data['password']

    #일단은 보안고려 없이 간단히 아이디와 비밀번호가 일치하면 로그인시킨다.
    user=Account.objects.filter(userId=userId).values()
    if user:
        #이제 여기서 유저 정보를 사용하여 추천할만한 복지정보를 필터링해 제공해야한다.

        #로그인 처리
        if user[0]['password']==password:
            return JsonResponse({
                'success':True,
                'userId':user[0]['userId'],
                'name':user[0]['name'],
            })
        else:
            return JsonResponse({
                'success':False,
                'type':'incorrectPW'
            })
    else:
        return JsonResponse({
            'success':False,
            'type':'noUser'
        })