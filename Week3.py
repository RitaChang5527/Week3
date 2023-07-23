#* task1
print("==============Task1==============")
import urllib.request
import json
import csv

#* 定義函式從網址取得資料
def fetch_data(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        return data
    except Exception as e:
        print("無法從網址取得資料：", e)
        return None

url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment.json"
data = fetch_data(url)

if data:
    try:
        #* 解析 JSON 資料
        json_data = json.loads(data)

        #* 1. 輸出 attraction.csv
        with open("attraction.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            header = ["Name","District", "Longitude", "Latitude", "Image"]
            writer.writerow(header)  #* 寫入欄位名稱
            for item in json_data["result"]["results"]:
                name = item["stitle"]
                address = item["address"]
                #* 從地址中提取區域資訊
                district = ""
                if "市" in address:
                    district = address.split("市")[1].split("區")[0].strip() + "區"
                else:
                    district = address.split("區")[0].strip() + "區"
                longitude = item["longitude"]
                latitude = item["latitude"]
                image_url = "https" + item["file"].split("https")[-1].split("?")[0].strip()  # 取得圖片網址，並刪除可能的參數

                # 篩選是否為相片（以.jpg、.png、.jpeg 結尾）
                if image_url.endswith((".jpg", ".JPG",".png", ".jpeg")):
                    writer.writerow([name, district, longitude, latitude, image_url])
        print("attraction.csv 檔案已成功輸出。")

        #* 2. 輸出 mrt.csv
        mrt_data = {}  #* 用來存放各捷運站的景點名稱
        for item in json_data["result"]["results"]:
            name = item["stitle"]
            mrt_stations = item.get("MRT")
            if mrt_stations is not None:
                mrt_stations = mrt_stations.split("、")
                for station in mrt_stations:
                    #* 將景點名稱按照捷運站分群
                    if station not in mrt_data:
                        mrt_data[station] = []
                    mrt_data[station].append(name)

        with open("mrt.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            header = ["捷運站名稱", "景點名稱"]
            writer.writerow(header)  #* 寫入欄位名稱
            for station, attractions in mrt_data.items():
                writer.writerow([station, *attractions])

        print("mrt.csv 檔案已成功輸出。")

    except json.JSONDecodeError as e:
        print("JSON 解析錯誤：", e)

#*task2
print("==============Task2==============")
import urllib.request as req
import bs4
import csv

url = "https://www.ptt.cc/bbs/movie/index.html"
request = req.Request(url, headers={
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
})

with req.urlopen(request) as response:
    data = response.read().decode("utf-8")

root = bs4.BeautifulSoup(data, "html.parser")
articles = root.find_all("div", class_="r-ent")

with open("movie.txt", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    header = ["文章標題", "推文數量", "發佈時間"]
    writer.writerow(header)  # 寫入欄位名稱

    for article in articles:
        title_element = article.find("div", class_="title")
        nrec_element = article.find("div", class_="nrec")

        if title_element and title_element.a:
            article_url = "https://www.ptt.cc" + title_element.a["href"]
            article_request = req.Request(article_url, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36"
            })

            with req.urlopen(article_request) as article_response:
                article_data = article_response.read().decode("utf-8")

            article_root = bs4.BeautifulSoup(article_data, "html.parser")
            meta_values = article_root.find_all("span", class_="article-meta-value")

            if len(meta_values) >= 4:
                title_text = title_element.a.text.strip()
                push_count = nrec_element.span.text.strip() if nrec_element and nrec_element.span else "0"
                post_time = meta_values[3].text.strip()
                writer.writerow([title_text, push_count, post_time])

print("movie.txt 檔案已成功輸出")


