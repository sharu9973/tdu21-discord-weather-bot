import requests
import datetime


class JMA:
    """
    気象庁APIを叩く、パースして取り出す
    """

    def __init__(self, area_code: int):
        self.area_code = area_code
        self.data = self.__fetch_forecast()

    def __fetch_forecast(self):
        self.end_pint = (
            f"https://www.jma.go.jp/bosai/forecast/data/forecast/{self.area_code}.json"
        )

        res = requests.get(self.end_pint)

        if res.status_code == 200:
            return res.json()

    def weather_text(self) -> str:
        return self.data[0].get("timeSeries")[0].get("areas")[0].get("weathers")[0]

    def pops(self) -> list:
        return self.data[0].get("timeSeries")[1].get("areas")[0].get("pops")

    def temps(self) -> list:
        return self.data[0].get("timeSeries")[2].get("areas")[0].get("temps")

    def date(self) -> str:
        iso_dt = self.data[0].get("reportDatetime")
        dt = datetime.datetime.fromisoformat(iso_dt)
        date_text = f"{dt.year}年{dt.month}月{dt.day}日{dt.hour}時"
        return date_text

    def office(self) -> str:
        return self.data[0].get("publishingOffice")

    def week_weather_codes(self) -> list:
        return self.data[1].get("timeSeries")[0].get("areas")[0].get("weatherCodes")

    def week_time_defines(self):
        return self.data[1].get("timeSeries")[0].get("timeDefines")