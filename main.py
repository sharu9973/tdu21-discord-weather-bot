import requests
import datetime


class FORECAST:
    """
    データを取りだしやすくするためだけのクラス
    クラスにする意味がなさそう
    """

    def __init__(self, data) -> None:
        self.data = data

    def weather_text(self) -> str:
        return self.data.get("timeSeries")[0].get("areas")[0].get("weathers")[0]

    def pops(self) -> list:
        return self.data.get("timeSeries")[1].get("areas")[0].get("pops")

    def temps(self):
        return self.data.get("timeSeries")[2].get("areas")[0].get("temps")

    def date(self) -> str:
        iso_dt = self.data.get("reportDatetime")
        dt = datetime.datetime.fromisoformat(iso_dt)
        date_text = f"{dt.year}年{dt.month}月{dt.day}日{dt.hour}時"
        return date_text

    def office(self):
        return self.data.get("publishingOffice")


def overview(path_code):
    OVERVIEW_END_POINT = (
        f"https://www.jma.go.jp/bosai/forecast/data/overview_forecast/{path_code}.json"
    )

    res = requests.get(OVERVIEW_END_POINT)
    data = res.json()

    return data.get("headlineText")


def main(**kwargs):
    path_code = kwargs["area_code"]
    END_POINT = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{path_code}.json"

    res = requests.get(END_POINT)

    if res.status_code == 200:
        data = FORECAST(res.json()[0])

        forecast_pops = data.pops()

        # 上の方の情報
        header_text = f"{data.date()}　{data.office()}　発表"
        campus_location = kwargs["name"]

        # 気温
        # 朝方なので最低気温はなしになる
        low_temp = data.temps()[0]
        high_temp = data.temps()[1]

        # 降水確率
        # データが右詰めなのでいい感じに格納する

        # 当日分だけを格納するリストを用意します
        pops_list = ["-"] * 4
        mod = len(forecast_pops) % 4
        for i, sec in enumerate(reversed(forecast_pops[0:mod])):
            # 後ろから格納
            pops_list[-(1 + i)] = str(sec)

        rainy_00 = pops_list[0]
        rainy_06 = pops_list[1]
        rainy_12 = pops_list[2]
        rainy_18 = pops_list[3]

        # headlineTextがない場合もあるので……
        # overview_headline_text = ""
        # if not (ht := overview(path_code)) == "":
        #     print(ht)
        #     overview_headline_text = f"⚠️ {ht} ⚠️"

        weather_text = data.weather_text().replace("　", " ")

        text = f"""
【{header_text}】
☀️ **{campus_location}キャンパスの天気** ☀️

📌 {weather_text} 📌

🌡️ 最高気温 🌡️
{high_temp} ℃

🌧️ 降水確率(％) 🌧️
🕛 00 - 06 : {rainy_00}
🕕 06 - 12 : {rainy_06}
🕛 12 - 18 : {rainy_12}
🕕 18 - 24 : {rainy_18}

        """

        print(text)
        return text


if __name__ == "__main__":
    campus_list = [
        {"name": "東京千住", "area_code": 130000, "channel_id": 833365284106272788},
        {"name": "埼玉鳩山", "area_code": 110000, "channel_id": 811620030604115969},
    ]

    for campus in campus_list:
        main(**campus)
