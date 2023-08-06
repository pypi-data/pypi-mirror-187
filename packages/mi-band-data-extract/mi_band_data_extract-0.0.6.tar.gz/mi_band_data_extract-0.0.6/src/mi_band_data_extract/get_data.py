import requests
import pandas as pd
import urllib
from ensure import ensure_annotations

APP_NAME = "com.xiaomi.hm.health"
APP_PLATFORM = "web"
BASE_URL = "https://api-mifit.huami.com"
endpoint = "/v1/sport/run/history.json"


@ensure_annotations
def get_data(args):

    access_token = input("Please input your access token: ")

    response = requests.get(
        urllib.parse.urljoin(BASE_URL, endpoint),
        headers={
            "apptoken": access_token,
            "appPlatform": APP_PLATFORM,
            "appname": APP_NAME,
        },
        params={},
    )

    data = pd.DataFrame(response.json()["data"]["summary"])
    print(data.head())
    data.to_csv("workouts.csv", index=False, header=True)
