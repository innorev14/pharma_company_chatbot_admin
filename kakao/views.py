from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse  # 카카오톡과 연동하기 위해선 JsonResponse로 출력
from django.views.decorators.csrf import csrf_exempt  # 보안 이슈를 피하기 위한 csrf_exempt decorator 필요
import json

from django.views.decorators.http import require_POST

from medicine.models import *


# JsonResponse 출력 테스트용
@csrf_exempt
def keyboard(request):
    return JsonResponse({'type': 'text'})

@require_POST
@csrf_exempt
def keyboard2(request):
    if request.method == 'POST':
        answer = request.body.decode('utf-8')
        return_json_str = json.loads(answer)
        return_str = return_json_str['userRequest']['utterance']
        print("전체 : ", return_json_str)
        print("발화 : ", return_str)

        text = {
            'version': "2.0",
            'template': {
                'outputs': [{
                    'simpleText': {
                        'text': "테스트 성공입니다."
                    }
                }],
                'quickReplies': [{
                    'label': '처음으로',
                    'action': 'message',
                    'messageText': '처음으로'
                }]
            }
        }

        if return_str == '테스트\n':
            return JsonResponse(text, status=200)
        else:
            return HttpResponse(status = 403)


@csrf_exempt
def medicine(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    user_input = json_req['userRequest']['utterance']  # 유저 발화
    user_id = json_req['userRequest']['user']['id']  # 유저 ID

    # 유저 확인 로직

    # 제품 정보 확인
    medicine_info = Medicine.objects.get(name=user_input)

    text = {
        'version': "2.0",
        'template': {
            'outputs': [{
                'simpleText': {
                    'text': medicine_info.product_info
                }
            }],
            'quickReplies': [{
                'label': '처음으로',
                'action': 'message',
                'messageText': '처음으로'
            }]
        }
    }

    return JsonResponse(text, status=200)



