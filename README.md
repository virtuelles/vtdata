# vtdata
完成度還差很遠,堪用而已
## Youtube API 金鑰取得參考
https://blog.jiatool.com/posts/youtube_spider_api/  
推薦多申請幾個放到這裡，金鑰一天配額有上限，不過streamdata.py對配額的消耗不高  
偶爾上google cloud platform確認消耗了多少就行  
https://console.cloud.google.com/iam-admin/quotas?service=youtube.googleapis.com
```
API_KEY = ['XXXXX','XXXXX']
```
## streamdata使用教學
環境:python 3
```
cd 到放程式碼的資料夾
python streamdata.py
依照填了多少個API金鑰從序號0開始選擇金鑰
輸入直播ID，也就是youtube網址最後面那個
例如 https://www.youtube.com/watch?v=dQw4w9WgXcQ 就是 dQw4w9WgXcQ
```
有顯示下圖這樣就是有在正常跑，請確保網路穩定，呼叫失敗會報錯  
![](https://i.imgur.com/HDk2gVl.png)  
輸出如下圖  
![](https://i.imgur.com/vMPjGTb.png)  
![](https://i.imgur.com/Urn42L0.png)  
> vtdata(或是看你想放在哪個資料夾)
>> 頻道名稱資料夾
>>> 直播標題資料夾
>>>> info of 本次直播資訊.txt  
>>>> 本次直播同時觀看人數、播放數、喜歡數、不喜歡數紀錄.csv 

## Todo
- [X] 時間格式整理
- [ ] 捕捉自動化
- [ ] 自動輸出繪圖
- [ ] 例外處理
- [ ] 留言、會員、SC統計
- [ ] 聊天室國籍組成
- [ ] 影片播放數紀錄
- [ ] 網頁化
- [ ] twitter bot
- [ ] discord bot
