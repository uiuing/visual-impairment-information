import json

from flask_cors import CORS

from controller.image import img_to_text
from controller.news import randomly_classified_news
from flask import Flask, request, config

from controller.voice import text_to_voice, voice_to_text

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.config.from_object(config)


def post_parse(post_request):
    data = post_request.get_data()
    return json.loads(data)


def get_parse(get_request):
    data = get_request.args
    return data


@app.route("/api/news/randomly", methods=['GET'])
def get_randomly_classified_news():
    data = get_parse(request)
    if "channel" in data and "num" in data:
        return json.dumps(randomly_classified_news(data['channel'], data['num']))
    return "error"


@app.route("/api/voice/text", methods=['GET'])
def get_voice():
    voice_types = {
        "新闻": 101011,
        "助手": 101007,
    }
    data = get_parse(request)
    if "text" in data and "voiceType" in data:
        return text_to_voice(data['text'], voice_types[data['voiceType']])
    return "error"


@app.route('/api/voice/voice', methods=['POST'])
def get_text():
    data = post_parse(request)
    if "voiceBase64" in data:
        return voice_to_text(data['voiceBase64'])
    return "error"


@app.route("/api/image/text", methods=['POST'])
def get_image():
    data = post_parse(request)
    if "imgBase64" in data:
        return img_to_text(data['imgBase64'])
    return "error"
