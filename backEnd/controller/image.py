import json
import random
import re

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


def img_to_text(img_base64):
    try:
        cred = credential.Credential("", "")
        http_profile = HttpProfile()
        http_profile.endpoint = "ocr.tencentcloudapi.com"

        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", client_profile)

        req = models.GeneralBasicOCRRequest()
        params = {
            "ImageBase64": img_base64,
        }
        req.from_json_string(json.dumps(params))

        resp = client.GeneralBasicOCR(req)

        text_detections = json.loads(resp.to_json_string())['TextDetections']

        # 遍历text_detections，判断DetectedText是否长度大于3，如果是，则保存
        result = {"result": []}
        for text_detection in text_detections:
            if len(text_detection['DetectedText']) > 3:
                result["result"].append(text_detection['DetectedText'])
        return result

    except TencentCloudSDKException as err:
        print(err)
