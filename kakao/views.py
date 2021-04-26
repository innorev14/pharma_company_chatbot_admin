import re
from urllib import parse

from django.contrib.auth import get_user_model
from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse  # 카카오톡과 연동하기 위해선 JsonResponse로 출력
from django.views.decorators.csrf import csrf_exempt  # 보안 이슈를 피하기 위한 csrf_exempt decorator 필요
import json

from django.views.decorators.http import require_POST

from accounts.models import User
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

        if return_str == '테스트':
            return JsonResponse(text, status=200)
        else:
            return HttpResponse(status=403)


@require_POST
@csrf_exempt
def welcome(request):
    if request.method == 'POST':
        send_msg = {
            'version': "2.0",
            'template': {
                'outputs': [
                    {
                        "simpleImage": {
                            "imageUrl": "https://cdn.imweb.me/thumbnail/20171207/5a28873a44a07.png",
                            "altText": "일화로고"
                        },
                        "description": "안녕하세요. 일화제약 제품 안내 챗봇입니다. 최초 인증을 진행해주세요.",
                        "buttons": [
                            {
                                "action": "block",
                                "label": "인증하기",
                                "blockId": "5fffb748e301aa34ff3c0230"
                            },
                        ]
                    }
                ]
            }
        }

        return JsonResponse(send_msg, status=200)


@require_POST
@csrf_exempt
def validation(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    phone = json_req['value']['origin']
    print(json_req)
    print(phone)
    vali_num = r"^\d{10,11}$"
    vali_num2 = r"^\d{3}-\d{3,4}-\d{4}$"
    vali_num3 = r"^\d{3}.\d{3,4}.\d{4}$"
    if re.match(vali_num, phone):
        send_msg = {
            "status": "SUCCESS",
            "value": phone,
        }
    elif re.match(vali_num2, phone):
        send_msg = {
                    "status": "SUCCESS",
                    "value": phone.replace('-', ''),
        }
    elif re.match(vali_num2, phone):
        send_msg = {
                    "status": "SUCCESS",
                    "value": phone.replace('.', ''),
        }
    else:
        send_msg = {
                    "status": "FAIL",
                    "value": phone,

                    "message": "전화번호가 형식이 올바르지 않습니다. \n\n"
        }

    print(send_msg)
    return JsonResponse(send_msg, status=200)


@require_POST
@csrf_exempt
def auth(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    user_id = json_req['userRequest']['user']['id']  # 유저 ID
    user_phone = json_req['contexts'][0]['params']['phone']['value']
    print(json_req)
    print(user_id)
    print(user_phone)

    user = get_user_model()

    try:
        match_user = user.objects.get(phone=user_phone)
        if match_user.kakao_id == '':
            match_user.kakao_id = user_id
            match_user.save()
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "인증되었습니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=200)
        else:
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "인증에 실패했습니다. 관리자에게 문의 바랍니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=403)
    except user.DoesNotExist:
        send_msg = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "사용자 정보가 미등록 되었습니다. 관리자에게 문의바랍니다."
                        }
                    }
                ]
            }
        }
        return JsonResponse(send_msg, status=403)


@require_POST
@csrf_exempt
def medicine(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    # user_input = json_req['userRequest']['utterance'][:-1]  # 유저 발화
    user_input = json_req['action']['params']['product_name']
    user_id = json_req['userRequest']['user']['id']  # 유저 ID
    print(json_req)
    print(user_id)
    print(user_input)
    user = get_user_model()

    try:
        # 유저 확인 로직
        check_id = user.objects.get(kakao_id=user_id)
        if check_id.group_is_active == 1 or check_id.is_active == 1:
            # 제품 정보 확인
            medicine_info = Medicine.objects.get(name=user_input)
            medicine_name = medicine_info.name.replace(' ', '')

            send_msg = {
                'version': "2.0",
                'template': {
                    'outputs': [
                        {
                            "simpleImage": {
                                "imageUrl": "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/"
                                            + parse.quote(medicine_name) + ".jpg",
                                "altText": "제품이미지"
                            },
                            "buttons": [
                                {
                                    "action": "block",
                                    "label": "제품정보",
                                    "blockId": "607e7831f1a09324e4b37a19"
                                },
                                {
                                    "action": "block",
                                    "label": "보험정보",
                                    "blockId": "6007a3be70fd446fa256b643"
                                },
                                {
                                    "action": "block",
                                    "label": "디테일 포인트",
                                    "blockId": "6007a3c83d34416490cf7ba7"
                                }
                            ]
                        }
                    ]
                }
            }

            return JsonResponse(send_msg, status=200)
        else:
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=403)
    except user.DoesNotExist:
        send_msg = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                        }
                    }
                ]
            }
        }
        return JsonResponse(send_msg, status=403)


@require_POST
@csrf_exempt
def prod_info(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    # user_input = json_req['userRequest']['utterance'][:-1]  # 유저 발화
    user_input = json_req['contexts'][0]['params']['product_name']['value']
    user_id = json_req['userRequest']['user']['id']  # 유저 ID
    print(json_req)
    print(user_id)
    print(user_input)
    user = get_user_model()

    try:
        # 유저 확인 로직
        check_id = user.objects.get(kakao_id=user_id)
        if check_id.group_is_active == 1 or check_id.is_active == 1:
            # 제품 정보 확인
            medicine_info = Medicine.objects.get(name=user_input)
            medicine_name = medicine_info.name.replace(' ', '')

            res = {
                'version': "2.0",
                'template': {
                    'outputs': [
                        {
                            "basicCard": {
                                "thumbnail": {
                                    "imageUrl": "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/image/"
                                                + parse.quote(medicine_info) + ".jpg",
                                },
                                "description": medicine_info.product_info.replace("<p>", "\n"),
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "상세보기",
                                        "webLinkUrl": medicine_info.product_url
                                    },
                                ]
                            },
                        }
                    ]
                }
            }
            return JsonResponse(res, status=200)
        else:
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=403)
    except user.DoesNotExist:
        send_msg = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                        }
                    }
                ]
            }
        }
        return JsonResponse(send_msg, status=403)

@require_POST
@csrf_exempt
def insu_info(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    # user_input = json_req['userRequest']['utterance'][:-1]  # 유저 발화
    user_input = json_req['contexts'][0]['params']['product_name']['value']
    user_id = json_req['userRequest']['user']['id']  # 유저 ID
    print(json_req)
    print(user_id)
    print(user_input)
    user = get_user_model()

    try:
        # 유저 확인 로직
        check_id = user.objects.get(kakao_id=user_id)
        if check_id.group_is_active == 1 or check_id.is_active == 1:
            # 제품 정보 확인
            medicine_info = Medicine.objects.get(name=user_input)
            medicine_name = medicine_info.name.replace(' ', '')

            res = {
                'version': "2.0",
                'template': {
                    'outputs': [
                        {
                            "basicCard": {
                                "thumbnail": {
                                    "imageUrl": "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/image/"
                                                + parse.quote(medicine_info) + ".jpg",
                                },
                                "description": medicine_info.insurance_info.replace("<p>", "\n"),
                            }
                        }
                    ]
                }
            }

            return JsonResponse(res, status=200)
        else:
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=403)
    except user.DoesNotExist:
        send_msg = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                        }
                    }
                ]
            }
        }
        return JsonResponse(send_msg, status=403)


@require_POST
@csrf_exempt
def detail_point(request):
    user_req = request.body.decode('utf-8')
    json_req = json.loads(user_req)
    # user_input = json_req['userRequest']['utterance'][:-1]  # 유저 발화
    user_input = json_req['contexts'][0]['params']['product_name']['value']
    user_id = json_req['userRequest']['user']['id']  # 유저 ID
    print(json_req)
    print(user_id)
    print(user_input)
    user = get_user_model()

    try:
        # 유저 확인 로직
        check_id = user.objects.get(kakao_id=user_id)
        if check_id.group_is_active == 1 or check_id.is_active == 1:
            # 제품 정보 확인
            medicine_info = Medicine.objects.get(name=user_input)
            medicine_name = medicine_info.name.replace(' ', '')

            res = {
                'version': "2.0",
                'template': {
                    'outputs': [
                        {
                            "basicCard": {
                                "thumbnail": {
                                    "imageUrl": "https://ilhwa-pharm.s3.ap-northeast-2.amazonaws.com/image/"
                                                + parse.quote(medicine_info) + ".jpg",
                                },
                                "description": medicine_info.detail_info.replace("<p>", "\n"),
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "상세보기",
                                        "webLinkUrl": medicine_info.detail_url
                                    }
                                ]
                            }
                        }
                    ]
                }
            }

            return JsonResponse(res, status=200)
        else:
            send_msg = {
                "version": "2.0",
                "template": {
                    "outputs": [
                        {
                            "simpleText": {
                                "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                            }
                        }
                    ]
                }
            }
            return JsonResponse(send_msg, status=403)
    except user.DoesNotExist:
        send_msg = {
            "version": "2.0",
            "template": {
                "outputs": [
                    {
                        "simpleText": {
                            "text": "권한이 없습니다. 관리자에게 문의 바랍니다."
                        }
                    }
                ]
            }
        }
        return JsonResponse(send_msg, status=403)