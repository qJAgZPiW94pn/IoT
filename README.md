# IoT
**智慧魚缸**
---
Observe the enviroment tempurature around the fish tank sensor of Raspberry pi, and use LINE communication software to control USB lighting, feeder, obtain historical temperature and humidity on Cacti and real-tiime images.


---
實際照片
---


---
影片連結
---


---
使用硬體材料
---
* Raspberry pi 4b *1
* DHT22 Temperature Humidity Sensor Module *1 https://www.sparkfun.com/products/10167
* 外接USB LED燈

---
使用軟體
---
Python 3.7.3 https://www.python.org/
Apache 2.4.38 https://httpd.apache.org/
Cacti 1.2.2 https://www.cacti.net/
Mariadb 10.3.31 https://mariadb.org/
LINE Bot Message API https://developers.line.biz/zh-hant/services/messaging-api/



---
Step 1. 溫溼度感測器安裝及收集歷史資料
---
1. 連接DHT22溫溼度感測器，根據腳位上方描述接到Raspberry pi上對應的腳位並調整程式碼
VCC -> power 正極
GND -> Ground 負極
DAT -> GPIO 收資料
NC -> 不用接

2. 參考以下網頁進行安裝cacti(記錄歷史溫溼度使用)、設定排程收集資料、上傳cacti、設定cacti看得懂的資料格式
> Raspberry Pi 搭配Cacti監控溫濕度
> https://kingfff.blogspot.com/2018/05/raspberry-pi-cacti-weather-dht22-temperature-humidity.html

* 安裝時發現網頁中所提供之套件Adafruit_DHT已不再維護，目前已改用Adafruit CircuitPython
> Adafruit_DHT 顯示DEPRECATED LIBRARY Adafruit Python DHT Sensor Library
> https://github.com/adafruit/Adafruit_Python_DHT
> 
> Adafruit CircuitPython
> https://github.com/adafruit/circuitpython


Step 2. 外接USB燈源及控制開啟或關閉
---
1. 程式碼參考uhubctl github 因為我是用Raspberry pi所以只用到以下列出的部份，針對不同作業系統甚至不同Raspberry pi版本有不同的安裝或者執行方式。
>  uhubctl github
>  https://github.com/mvp/uhubctl 

* To fetch uhubctl source and compile it:
```
git clone https://github.com/mvp/uhubctl
cd uhubctl
make
```
* This should generate uhubctl binary. You can install it in your system as /usr/sbin/uhubctl using:
```
sudo make install
```
2. 最後依照上方github說明使用指令控制USB供電以達到外接LED燈開啟或關閉的效果
* USB off
```
sudo uhubctl -l 2 -a 0
```
* USB on
```
sudo uhubctl -l 2 -a 1
```

Step 3. 使用LINE Message API實現手機控制Raspberry pi
---
* 參考LINE Document，此次只用到Text message及Image message
> LINE Message type introduction
> https://developers.line.biz/en/docs/messaging-api/message-types/ 

1. Message API申請方式及ngrok建置方式參考以下網址進行申請及建置，ngrok用途為使Raspberry pi與外界溝通，以達成接收及傳送LINE訊息的目的
> Rasbperry Pi 結合 LINE messaging API
> https://blog.cavedu.com/2021/12/06/rasbperry-pi-line-messaging-api/ 

2. 程式部分LINE github即有完整Example可參考，實際使用範例主要參考日文網頁中鑰匙開關之控制方式。
>  line-bot-sdk-python
>  https://github.com/line/line-bot-sdk-python 
>  
>  在 LINE 上解鎖和開鎖 (日文)
>  https://qiita.com/t-funaki/items/2a3bbed8f63d2dc660a3 


Step 4. LINE Message API 回傳即時溫度 (Text message)
---
1. 參考以下日文網頁，調整一下在收到指定訊息時呼叫function取得dht22的即時溫度及回傳
> 在 LINE 上解鎖和開鎖 (日文)
> https://qiita.com/t-funaki/items/2a3bbed8f63d2dc660a3 

程式主要部份：
* main
```
if message.count("顯示現在溫度"):
    temperature = function.temperature()
    line_bot_api.reply_message(event.reply_token,
    TextSendMessage(text="現在溫度是" + str(temperature) + "度C"))
```

* function
```
dht = adafruit_dht.DHT22(board.D4)
def temperature():
    temperature = dht.temperature
    humidity = dht.humidity
    return temperature
```

Step 5. LINE Message API 回傳歷史溫度紀錄 (Image message)
---
* 根據LINE Message API documentation說明，Bot回傳的Image URL必須使用HTTPS及TLS 1.2 或更高版本，並且僅能傳送PNG或是JPEG檔案。
> Image message說明
> https://developers.line.biz/en/reference/messaging-api/#image-message

* 嘗試過想要把圖檔丟到免費的 Imgur.com 再回傳但一直失敗，下面提供的兩種方法我都試過，都遇到上傳失敗或是找不到module的問題，最後想到直接用ngrok的那個動態網址丟回去。
> 用 Python 上傳圖片至 Imgur 圖床 (試不成功)
> https://ithelp.ithome.com.tw/articles/10241006

1. 為了達成自動化取得ngrok URL的目的，接收到指定訊息時必須呼叫function取得URL再寫到後續的code裡面。
> 取得ngrok URL的方式
>  https://stackoverflow.com/questions/34322988/view-random-ngrok-url-when-run-in-background
    
2. 有了URL之後必須將cacti中所收集的dht22歷史溫溼度圖片取回來才能發送回去，因此這邊執行了另一支python(download_graph_45)將cacti上的圖取回放在static資料夾。
>　這個部份參考如下網址，但在Google上搜尋有多個相同的網頁，不確定這網址是否為真。
>https://www.itread01.com/p/456374.html
> 
> 另一個更簡單的方法：
> cacti免登入檢視graph
>  https://blog.xuite.net/jyoutw/xtech/536474338-Cacti+%E5%85%8D%E7%99%BB%E5%85%A5%E6%AA%A2%E8%A6%96+Graph


* 在cacti圖片上點右鍵Graph -> Copy graph link可查看圖片編號
![](https://i.imgur.com/XtKJgXm.png)

* URL說明如下：
local_graph_id -> 這張圖片ID
graph_start -> 圖片開始時間
graph_end -> 圖片結束時間
graph_width=414 -> 圖片寬度
graph_height -> 圖片高度
```
http://localhost/cacti/graph_image.php?local_graph_id=45&graph_start=1641882527&graph_end=1641968927&graph_width=414&graph_height=99
```

3. 後續和Text message差不多，Text部份是使用Token+Text，圖片部份就是換成token+URL回傳給使用者，其中URL我換成自動取到到ngrok URL，路徑則指向static資料夾下。
    

程式主要部份：
* main
```
elif message.count('顯示溫濕度紀錄'):
    ngrok_url = function.get_ngrok_url()
    exec(open("download_graph_45.py").read())
    line_bot_api.reply_message(event.reply_token,
    ImageSendMessage(original_content_url = ngrok_url + "/static/cacti_graph_45.png",
    preview_image_url = ngrok_url + "/static/cacti_graph_45.png"))
```

* function
```
def get_ngrok_url():
    url = "http://localhost:4040/api/tunnels"
    res = requests.get(url)
    res_unicode = res.content.decode("utf-8")
    res_json = json.loads(res_unicode)
    return res_json["tunnels"][0]["public_url"]
```


Step 6. 設定Rich menu
---
1. 這邊是設計Bot介面的圖文選單，我這邊直接用LINE線上的LINE offical Account Manager功能設計rich menu，這個方法最多可支援六個指令
![](https://i.imgur.com/DmBABFN.png)

* 設計好選單並上傳圖片後可依據不同位置設定要傳送的文字，Raspberry pi接收到指令後再搭配上面的程式執行不同動作
![](https://i.imgur.com/cbXHCRa.png)

> rich menu說明
> https://developers.line.biz/zh-hant/docs/messaging-api/using-rich-menus/#using-rich-menus-introduction
> 
> LINE offical Account Manager
> https://manager.line.biz/
> 
> PNG素材
> https://www.pngsucai.com/
>
> rich meau template
> https://static.line-scdn.net/biz-app/16bd9ea9e03/manager/static/LINE_rich_menu_design_template.zip

---

---
Reference
---
Adafruit_CircuitPython_DHT
https://github.com/adafruit/Adafruit_CircuitPython_DHT

Raspberry Pi 搭配Cacti監控溫濕度
https://kingfff.blogspot.com/2018/05/raspberry-pi-cacti-weather-dht22-temperature-humidity.html

LINE Messaging API SDK for Python
https://github.com/line/line-bot-sdk-python

Raspberry Pi 3+DHT22 で気温を通知するLINEbotを作る②
https://qiita.com/zakopuro/items/ed6720f4c27773cb58c7

LINEでおうちの鍵を開け締めする
https://qiita.com/t-funaki/items/2a3bbed8f63d2dc660a3

uhubctl - USB hub per-port power control
https://github.com/mvp/uhubctl

Rasbperry Pi 結合 LINE messageing API
https://blog.cavedu.com/2021/12/06/rasbperry-pi-line-messaging-api/

PNG素材
https://www.pngsucai.com/

View random ngrok URL when run in background
https://stackoverflow.com/questions/34322988/view-random-ngrok-url-when-run-in-background

Line Messaging API 的各種訊息格式
https://ithelp.ithome.com.tw/articles/10198142

python 自動登陸cacti獲取主機流量圖
https://www.itread01.com/p/456374.html

PiCamera & Python – How to add text on images and video
https://www.meccanismocomplesso.org/en/picamera-python-how-to-add-text-on-images-and-video/

TAIWANIOT
https://www.taiwaniot.com.tw/
