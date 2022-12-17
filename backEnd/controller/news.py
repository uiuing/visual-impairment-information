import random

import requests as requests


def randomly_classified_news(channel, num):
    random_num = random.randint(0, 300)
    request = requests.get("https://way.jd.com/jisuapi/get", params={
        "appkey": "",
        "channel": channel,
        "num": num*5,
        "start": random_num,
    })
    news_list = request.json()["result"]["result"]["list"]
    news_list = random.sample(news_list, int(num))
    for i in range(len(news_list)):
        news_list[i]["content"] = news_list[i]["content"].replace("<img", "<img style=\"width:100%\"")
        news_list[i]["content"] = news_list[i]["content"].replace("<video", "<video style=\"width:100%\"")
        news_list[i]["content"] = news_list[i]["content"].replace("<h2", "<p class=\"art_p\" style=\"font-size:2px;\"")
        news_list[i]["content"] = news_list[i]["content"].replace("</h2>", "</p>")
        news_list[i]["content"] = news_list[i]["content"].replace("<a", "<p")
        news_list[i]["content"] = news_list[i]["content"].replace("</a>", "</p>")
        news_list[i]["content"] = news_list[i]["content"].replace("class=\"", "old-class=\"")
        news_list[i]["content"] = news_list[i]["content"].replace("<p", "<p class=\"label-is-readable readable-par\" "
                                                                        "label-is-readable=\"true\"")

        news_time = news_list[i]["time"]
        news_time_dt = news_time.split(" ")
        # 年月日安装-分割
        news_time_d = news_time_dt[0].split("-")
        if len(news_time_dt) == 1:
            news_list[i]["time"] = news_time_d[0] + "年" + news_time_d[1] + "月" + news_time_d[2] + "日"
            continue
        news_time_t = news_time_dt[1].split(":")
        news_list[i]["time"] = news_time_d[0] + "年" + news_time_d[1] + "月" + news_time_d[2] + "日" + " " + \
                               news_time_t[0] + "时" + news_time_t[1] + "分"
    return news_list
