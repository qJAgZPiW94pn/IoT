#/usr/bin/env python
# -*- coding: utf-8 -*- 
import time,datetime,socket
import urllib.request
import urllib.error
from http import cookiejar
#由於我是今天去取上周一的時間所以這裏寫成10，時間應該是2014年11月24上周星期一,
threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = 5)) 
#時間格式化輸出，由於cacti裏面的時間是以時間戳計算的我方便轉換成時間戳
otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S") 
print (otherStyleTime)
#由於上面取到的時間是以當前的時間跟日期，但是我cacti裏面出圖的時間應該從00:00:00開始，所以轉換
format_otherStyleTime = "%s 00:00:00" % otherStyleTime.split()[0]
print (format_otherStyleTime)
start=time.mktime(time.strptime(format_otherStyleTime,'%Y-%m-%d %H:%M:%S'))
print (start)

threeDayAgo = (datetime.datetime.now() - datetime.timedelta(days = -1))
otherStyleTime = threeDayAgo.strftime("%Y-%m-%d %H:%M:%S")
print (otherStyleTime)
result = "%s 00:00:00" % otherStyleTime.split()[0]
print (result)
end=time.mktime(time.strptime(result,'%Y-%m-%d %H:%M:%S'))

print (end)


socket.setdefaulttimeout(10)
headers = {
    "Accept" : "application/json, text/plain, */*",
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.7 Safari/537.36",
    "Accept-Language" : "zh-TW,zh;q=0.8"
}
#cookiejar = cookielib.CookieJar()
cookie = cookiejar.CookieJar()
#urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
urlOpener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))

# login
values = {'action':'login', 'login_username':'guest','login_password':'12345678' }
#data = urllib.parse.urlencode(values)
data = urllib.parse.urlencode(values).encode("utf-8")

request = urllib.request.Request("http://192.168.1.7/cacti/index.php", data, headers)
#request = urllib.request.Request("http://192.168.1.7/cacti/index.php", data=urllib.parse.urlencode(data).encode(encoding='UTF8'), headers=headers)
#res = urllib.request.urlopen(request).read().decode("utf-8")
#res = urlOpener.open(request).read()
res = urllib.request.urlopen(request).read()

#get image
request = urllib.request.Request("http://192.168.1.7/cacti/graph_image.php?local_graph_id=45&rra_id=0&view_type=tree&graph_start=%s&graph_end=%s&graph_width=800&graph_height=600"%(int(start),int(end)), None ,headers)
#request = urllib.request.Request("http://192.168.1.7/cacti/graph_image.php?local_graph_id=45&graph_start="%(int(start)"&graph_end=%s"%(int(end))"&graph_width=500&graph_height=120", None ,headers)
#res = urlOpener.open(request).read()

res = urllib.request.urlopen(request).read()

# save image to file
file_object = open('cacti_graph_45.png', 'wb')
file_object.write(res)
file_object.close()
print ("download completed")
