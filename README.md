# vtdata
完成度還差很遠,堪用而已  
20211223更新  
  dislike註解掉和調整  
  fileopen調整  
  info順序調整  
20210910更新  
  輸出圖片修改  
  livestream,countafterstream,collectall整理統一  
  livestream: 單爬直播數據  
  countafterstream: 單爬直播後一天數據,支援一般影片  
  collectall = livestream + countafterstream, 一次開一天以上  
## Youtube API 金鑰取得參考
https://blog.jiatool.com/posts/youtube_spider_api/  
推薦多申請幾個放到這裡，金鑰一天配額有上限，不過streamdata.py對配額的消耗不高  
不要用太多個,會被ban  
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
直播結束後或手動跳出時自動生成圖表  
![](https://i.imgur.com/cQUNW4T.png)  
> vtdata(或是看你想放在哪個資料夾)
>> 頻道名稱資料夾
>>> 直播標題資料夾
>>>> info of 本次直播資訊.txt  
>>>> 本次直播同時觀看人數、播放數、喜歡數、不喜歡數紀錄.csv  
>>>> chart of 本次直播圖表.png  

## countAfterStream使用教學
基本上操作一樣,也可用於爬取影片,輸出view,like,dislike,comment  
預設間格為10分鐘  
儲存位置相同  
![](https://i.imgur.com/C6Bmo99.png)  
> vtdata(或是看你想放在哪個資料夾)
>> 頻道名稱資料夾
>>> 直播標題資料夾
>>>> count after stream of 影片資訊.txt  
>>>> count after stream of view,like,dislike,comment.csv  
>>>> count chart after stream of 影片.png  

## collectall使用教學
就是全部合在一起跑,用一次要一天以上,調查影片觀看計算用  


## Todo
- [X] 時間格式整理
- [ ] 捕捉自動化
- [X] 自動輸出圖表
- [X] 例外處理
- [ ] 留言、會員、SC統計
- [ ] 聊天室國籍組成
- [X] 影片播放數紀錄
- [ ] 網頁化
- [X] twitter bot
- [X] discord bot
