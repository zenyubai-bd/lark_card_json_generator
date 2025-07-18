import json

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

import os
import shutil

PATH = os.getcwd()

######## SET the APP_ID and APP_SECRET ########
APP_ID = "cli_a8e1d9f91abb900c"
APP_SECRET = "jglESE0cQ2CpSUCPQitQhu0MUiUmVAOm"

################################################

def get_img_key(img):
    client = lark.Client.builder() \
        .app_id(APP_ID) \
        .app_secret(APP_SECRET) \
        .log_level(lark.LogLevel.DEBUG) \
        .build()

    file = open(img,"rb")
    request: CreateImageRequest = CreateImageRequest.builder() \
        .request_body(CreateImageRequestBody.builder()
            .image_type("message")
            .image(file)
            .build()) \
        .build()

    # 发起请求
    response: CreateImageResponse = client.im.v1.image.create(request)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.im.v1.image.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    image_key = response.data.image_key
    return image_key

