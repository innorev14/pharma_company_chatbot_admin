from django.shortcuts import render

from django.shortcuts import render
from django.http import JsonResponse  # 카카오톡과 연동하기 위해선 JsonResponse로 출력
from django.views.decorators.csrf import csrf_exempt  # 보안 이슈를 피하기 위한 csrf_exempt decorator 필요
import json

from medicine.models import *

# JsonResponse 출력 테스트용
def keyboard(request):
    return JsonResponse({'type': 'text'})


@csrf_exempt
def medicine(request):
    answer = (request.body.decode('utf-8'))
    return_json_str = json.loads(answer)  # json 포맷으로 카카오톡 내용 받아오기
    return_str = return_json_str['userRequest']['utterance']  # 사용자 발화 추출
    idx = return_str.index('을')
    disease = return_str[:idx]
    print(return_str)
    print(idx)
    print(disease)
    # manu = '제조사: '
    # effect = '효능효과 알아보기'
    # usage = '복용법 알아보기'
    # precautions = '주의사항 알아보기'
    # if return_str == disease + '을 위한 약품':  # 사용자 발화 예상
    #     can = medicine.objects.filter(disease=disease)  # 장고와 연동된 MySQL에서 데이터 가져오기
    #     return JsonResponse({
    #         "version": "2.0",
    #         "template": {
    #             "outputs": [{
    #                 "carousel": {  # 스킬가이드에 나온 캐러셀 형태
    #                     "type": "basicCard",  # 기본형 선택 (<->비즈니스형도 존재)
    #                     "items": [{
    #                         "title": can[0].medicine,  # 제목
    #                         "description": manu + can[0].manufacturer,  # 설명
    #                         "thumbnail": {  # 썸네일 이미지
    #                             "imageUrl": can[0].imgurl
    #                         }, "buttons": [  # 버튼 {
    #                             "action": "message",  # 동작 형태(텍스트 출력)
    #                                       "label": "효능효과",  # 버튼 이름
    #     "messageText": can[0].medicine + ' ' + effect
    #     },
    #     {
    #         "action": "message",
    #         "label": "복용법",
    #         "messageText": can[0].medicine + ' ' + usage},
    #     {
    #         "action": "message",
    #         "label": "주의사항",
    #         "messageText": can[0].medicine + ' ' + precautions
    #     }
    #     ]
    #     },
    #     {"title": can[1].medicine,
    #      "description": manu + can[1].manufacturer,
    #      "thumbnail": {"imageUrl": can[1].imgurl},
    #      "buttons": [{
    #          "action": "message",
    #          "label": "효능효과",
    #          "messageText": can[1].medicine + ' ' + effect
    #      },
    #          {
    #              "action": "message",
    #              "label": "복용법",
    #              "messageText": can[1].medicine + ' ' + usage
    #          },
    #          {
    #              "action": "message",
    #              "label": "주의사항",
    #              "messageText": can[1].medicine + ' ' + precautions
    #          }
    #      ]
    #      }, {
    #         "title": can[2].medicine,
    #         "description": manu + can[2].manufacturer,
    #         "thumbnail": {"imageUrl": can[2].imgurl},
    #         "buttons": [{
    #             "action": "message",
    #             "label": "효능효과",
    #             "messageText": can[2].medicine + ' ' + effect
    #         },
    #             {
    #                 "action": "message",
    #                 "label": "복용법",
    #                 "messageText": can[2].medicine + ' ' + usage
    #             },
    #             {
    #                 "action": "message",
    #                 "label": "주의사항",
    #                 "messageText": can[2].medicine + ' ' + precautions
    #             }
    #         ]
    #     ]
    #     }
    #     }
    #     ]
    #     }
    #     })
