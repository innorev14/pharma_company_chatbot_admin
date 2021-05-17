# -*- coding: utf-8 -*-
import requests
import json

from config.settings.base import get_secret


def get_token():
    basic_send_url = 'https://kakaoapi.aligo.in/akv10/token/create/1/h/'  # 요청을 던지는 URL, 현재는 토큰생성
    # token/create/토큰 유효시간/{y(년)/m(월)/d(일)/h(시)/i(분)/s(초)}/

    # ================================================================== 토큰 생성 필수 key값
    # API key, userid
    # API키, 알리고 사이트 아이디

    sms_data={'apikey': get_secret("ALIGO_APIKEY"), #api key
            'userid': get_secret("ALIGO_ID"), # 알리고 사이트 아이디
    }

    create_token_response = requests.post(basic_send_url, data=sms_data)
    print(create_token_response.json())

    return create_token_response.json()


def send_friend_msg(aligo_token, msg):
    basic_send_url = 'https://kakaoapi.aligo.in/akv10/friend/send/' # 요청을 던지는 URL, 친구톡 전송


    # ================================================================== 친구톡 보낼 때 필수 key값
    # API key, userid, token, senderkey, sender, receiver_1, subject_1, message_1
    # API키, 알리고 사이트 아이디, 토큰, 발신프로파일 키, 발신번호, 수신번호, 친구톡 제목, 친구톡 내용
    #
    # ================================================================== 친구톡 보낼 때 선택 key값
    # senddate, advert, image, image_url, recvname_1, button_1,
    # 예약일, 광고분류(기본Y), 첨부이미지, 첨부이미지에 삽입되는 링크,수신자 이름, 버튼 정보,
    # failover, fimage, fsubject_1, fmessage_1, testMode
    # 실패시 대체문자 {전송여부/첨부이미지/제목/내용}, 테스트 모드 적용 여부(기본N)
    #


    sms_data={'apikey': get_secret("ALIGO_APIKEY"),  #api key
            'userid': get_secret("ALIGO_ID"),  # 알리고 사이트 아이디
            'token': aligo_token['token'],  # 생성한 토큰
            'senderkey': get_secret("ALIGO_SENDERKEY"),  # 발신프로파일 키
            'sender' : msg['sender'],  # 발신자 연락처,
            #'senddate': '19000131120130',  # YYYYMMDDHHmmss
            'advert': 'N',  # 광고분류(기본Y)
            'receiver_1': msg['receiver'],  # 수신자 연락처
            #'recvname_1': '홍길동1', # 수신자 이름
            'subject_1': msg['content'][:30],  # 친구톡 제목
            'message_1': msg['content'],  # 친구톡 내용
            #'failover': 'Y or N', # 실패시 대체문자 전송 여부(템플릿 신청시 대체문자 발송으로 설정하였더라도 Y로 입력해야합니다.)
            #'fsubject_1': '대체문자 제목', # 실패시 대체문자 제목
            #'fmessage_1': '대체문자 내용', # 실패시 대체문자 내용
            #'testMode': 'Y or N' # 테스트 모드 적용여부(기본N), 실제 발송 X
            }

    try:
        # -------------------------------------------------------------------------------------------------
        # BUTTON
        #
        # name: 버튼명,
        # linkType: 버튼 링크타입(DS:배송조회, WL:웹링크, AL:앱링크, BK:봇키워드, MD:메시지전달),
        # linkTypeName : 버튼 링크 타입네임, ( 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개)
        # linkM: 모바일 웹링크주소(WL일 때 필수), linkP: PC웹링크 주소(WL일 때 필수),
        # linkI: IOS앱링크 주소(AL일 때 필수), linkA: Android앱링크 주소(AL일 때 필수)

        button_info = {'button': [{'name': msg['weblink']['btn_name'],  # 버튼명
                                   'linkType': 'WL',  # DS, WL, AL, BK, MD
                                   'linkTypeName': '웹링크',  # 배송조회, 웹링크, 앱링크, 봇키워드, 메시지전달 중에서 1개
                                   'linkM': msg['weblink']['mobile link'],  # WL일 때 필수
                                   'linkP': msg['web_link']['pc link']  # WL일 때 필수
                                   # 'linkI': 'IOS app link', # AL일 때 필수
                                   # 'linkA': 'Android app link' # AL일 때 필수
                                   }]}
        sms_data['button_1'] = button_info  # 버튼 정보
    except:
        pass

    try:
        sms_data['image_url'] = msg['img']['img_link']  # 첨부이미지에 삽입되는 링크

        images = {'image' : open(image['path'], 'rb')} # 첨부 이미지 경로
        # images.update({'fimage': open(image['path'], 'rb')}) # 실패시 첨부이미지 경로

        # =================================================================================================
        # 첨부 이미지 포함 전송
        friend_send_response = requests.post(basic_send_url, data=sms_data, files=images)

    except TypeError:
        # =================================================================================================
        # 첨부 이미지 없이 전송
        friend_send_response = requests.post(basic_send_url, data=sms_data)




    print(friend_send_response.json())

    return friend_send_response.json()


