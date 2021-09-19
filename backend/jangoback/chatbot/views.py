from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse
import dialogflow
import os
import json
from itertools import chain
from google.protobuf.json_format import MessageToJson
os.environ['DJANGO_SETTINGS_MODULE'] = 'jangoback.settings'
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

import django
django.setup()

from chatbot.models import Welfare

#텍스트 의도 탐지 함수
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result

#dialogflow로 사용자 입력을 전달하고, 그에대한 응답을 받아 리턴하는 함수 
def chat(request):
    req = json.loads(request.body)
    message = req['message']

    project_id = os.environ['DIALOGFLOW_PROJECT_ID']
    query_result = detect_intent_texts(project_id, "unique", message, 'ko')

    if query_result.all_required_params_present and query_result.intent.display_name!="Default Fallback Intent":
        jsonObj = MessageToJson(query_result)
        words=json.loads(jsonObj)["parameters"] 

        #Entity
        location=words['area']
        location_detail=words['area_detail']

        #domain이 여러개의 값을 가질 수 있다. [노년, 집] 또는 [청년, 주거] 처럼
        domain=words['UserWants']

        #복지 유형이 두개 이상인 경우
        if len(domain)>1:
            res1=Welfare.objects.all().values('location','location_detail','title','description','link').filter(location=location[0]).\
                filter(Q(location_detail=location_detail[0]) | Q(location_detail='본청')).filter(domain=domain[0])
        
            res2=Welfare.objects.all().values('location','location_detail','title','description','link').filter(location=location[0]).\
                filter(Q(location_detail=location_detail[0]) | Q(location_detail='본청')).filter(domain=domain[1])
        
            #두 유형 모두에 포함되는 요소
            bothHave=res1.intersection(res2)
            res=bothHave
            
            if domain[0] in ['영유아','아동·청소년','청년','중장년','노년']:
                diff=res.difference(res2)
                print(diff)
                res=list(chain(res,diff))
                
            else:
                diff=res.difference(res1)
                res=list(chain(res,diff))

        else:
            res=Welfare.objects.all().values().filter(location=location[0]).\
                filter(Q(location_detail=location_detail[0]) | Q(location_detail='본청')).filter(domain=domain[0])
            
        
        
        return JsonResponse({
            'message':'제공해주신 정보로 찾은 결과입니다 :)',
            'isLast':True,
            'data':list(res[:10])
        })

    #print(query_result.output_contexts[0].parameters.fields['UserWants'].list_value.values[0])
    fulfillment_text = query_result.fulfillment_text

    response = {"message":  fulfillment_text, "data":[]}

    #print(response)

    return JsonResponse(response)
