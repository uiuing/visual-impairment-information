import json
import random
import re

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tts.v20190823 import tts_client, models
from tencentcloud.asr.v20190614 import asr_client, models as asr_models


def text_to_voice(text, voice_type):
    try:
        cred = credential.Credential("", "")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tts.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = tts_client.TtsClient(cred, "ap-guangzhou", clientProfile)

        req = models.TextToVoiceRequest()
        params = {
            "Text": text,
            "VoiceType": voice_type,
            "Speed": -0.2,
            "Volume": 10,
            "SessionId": str(random.random())
        }
        req.from_json_string(json.dumps(params))

        resp = client.TextToVoice(req)
        return json.loads(resp.to_json_string())['Audio']

    except TencentCloudSDKException as err:
        print(err)


def voice_to_text(voice_base64):
    try:
        cred = credential.Credential("", "")
        httpProfile = HttpProfile()
        httpProfile.endpoint = "asr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = asr_client.AsrClient(cred, "", clientProfile)

        req = asr_models.SentenceRecognitionRequest()
        params = {
            "ProjectId": 0,
            "SubServiceType": 2,
            "EngSerViceType": "16k_zh_dialect",
            "SourceType": 1,
            "VoiceFormat": "wav",
            "UsrAudioKey": str(random.random()),
            "Data": voice_base64,
            "HotwordId": ""
        }
        req.from_json_string(json.dumps(params))

        resp = client.SentenceRecognition(req)
        print(resp.to_json_string())
        content = json.loads(resp.to_json_string())['Result']

        category_s = [
            "头条",
            "国内",
            "国际",
            "政治",
            "财经",
            "体育",
            "娱乐",
            "军事",
            "教育",
            "科技",
            "股票",
            "星座",
            "育儿",
            "新闻",
        ]

        if len(content) <= 1:
            return {"status": "error", "voice": text_to_voice("没有识别到您的语音，请您慢一点描述", 101007)}

        for i in category_s:
            if i in content:
                return {"status": "success", "c": "channel", "content": i}

        return {"status": "error", "voice": text_to_voice("对不起，没能理解您的意思", 101007)}

    except TencentCloudSDKException as err:
        print(err)
