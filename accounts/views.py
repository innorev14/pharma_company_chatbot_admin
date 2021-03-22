from django.shortcuts import render
from rest_framework.views import APIView


class KakaoAPIView(APIView):
    def post(self, request):
        print('request : ', request)
        req_kakao = request.POST.get()
        print('req_kakao : ', req_kakao)
        kakao_id = {
            'kakao_vlink': {'user_id': req_kakao['userRequest']['user']['id']}
        }
        print('kakao_id : ', kakao_id)
