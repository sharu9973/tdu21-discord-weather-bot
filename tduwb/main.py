import datetime
from .JMA import JMA
from .week import weather_code_text


class MainText:
    """送信するテキストを整形する"""

    def __init__(self, camplus_name: str, area_code: int, jma_link: str):
        self.campus_name = camplus_name
        self.jma_link = jma_link
        self.forecast_data = JMA(area_code)

    def main_text(self) -> str:
        """チャンネルに送信される本文テキスト"""

        data = self.forecast_data

        # 上の方の情報
        header_text = f"{data.date()} {data.office()} 発表"
        campus_location = self.campus_name

        # 気温
        # 朝方なので最低気温はなしになる
        low_temp = data.temps()[0]
        high_temp = data.temps()[1]

        # 降水確率
        # データが右詰めなのでいい感じに格納する
        forecast_pops = data.pops()

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

        weather_text = data.weather_text().replace("　", " ")

        text = f"""
【{header_text}】
☀️ **{campus_location}キャンパス周辺の天気** ☀️

📌 {weather_text} 📌

🌡️ 最高気温 🌡️
{high_temp} ℃

🌧️ 降水確率(％) 🌧️
🕛 00 - 06 : {rainy_00}
🕕 06 - 12 : {rainy_06}
🕛 12 - 18 : {rainy_12}
🕕 18 - 24 : {rainy_18}

▼ 詳細はこちら ▼
{self.jma_link}
            """

        return text

    def week_forecast(self) -> str:
        """チャンネルトピックに記載される週間予報テキスト"""

        weather_codes = self.forecast_data.week_weather_codes()
        times = self.forecast_data.week_time_defines()

        topic_text = ""

        for day, code in zip(times, weather_codes):

            date_list = ["月", "火", "水", "木", "金", "土", "日"]

            iso_dt = day
            dt = datetime.datetime.fromisoformat(iso_dt)
            day_text = f"{dt.day}日({date_list[dt.weekday()]})"

            forecast_text = weather_code_text(int(code))

            topic_text += f"""{day_text}
{forecast_text}
"""
        return topic_text
