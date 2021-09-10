# coding=utf-8
from datetime import *
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import datetime
import requests
import time
import csv
import os
import re

def localTimeClean(time):
    cleanAlphabet=re.sub('[A-Za-z]',' ',time)
    return cleanAlphabet

def APItimeSetToUTC8(time):
    cleanalpha=re.sub('[A-Za-z]',' ',time)
    strp=datetime.datetime.strptime(cleanalpha,"%Y-%m-%d %H:%M:%S ")
    toUTC8=strp + datetime.timedelta(hours = 8)
    return toUTC8

def sleep_time(hour, min, sec):
    return hour * 3600 + min * 60 + sec

def get_livestream_info(API_KEY,vID):
    '''
    Use "videos" function to derive info of livestream,可能另做一個專爬liveinfo的
    '''
    params = {
            'part': 'liveStreamingDetails,statistics,snippet',
            'key': API_KEY,
            'id': vID,
            'fields': 'items(id,liveStreamingDetails(activeLiveChatId,concurrentViewers,scheduledStartTime,actualStartTime,actualEndTime),' + 
            'snippet(channelId,channelTitle,liveBroadcastContent,publishedAt,title),statistics)'
            }
    headers = {'User-Agent': 'Chrome/92.0.4515.107'}
    url = 'https://www.googleapis.com/youtube/v3/videos'
    req = requests.get(url, headers=headers, params=params).json()
    
    streamData = dict(req.get('items')[0])
    
    return streamData

localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
localtime=localTimeClean(localtime)
print('運作開始時間start at(UTC+8): '+localtime)

#輸入API,可以多申請幾個使用
API_KEY = ['XXXXX','XXXXX']

apiKeySelect=int(input('選擇要使用的APIKEY(從0開始):'))
#輸入直播網址ID
vid=input('輸入直播ID:')
# 取得直播資訊
sinfo = get_livestream_info(str(API_KEY[apiKeySelect]),vid)


Channel=sinfo['snippet']['channelTitle']
channelFileName=re.sub('[\/:*?"<>|]',' ',Channel)

Video_ID=sinfo['id']
Stream_Created=sinfo['snippet']['publishedAt']
Stream_Created=APItimeSetToUTC8(Stream_Created)

#建立頻道資料夾
if os.path.isdir(channelFileName):
    os.chdir(channelFileName)
else:
    os.mkdir(channelFileName)
    os.chdir(channelFileName)

if "scheduledStartTime" in sinfo['liveStreamingDetails']:
    Planed_Start_Time=sinfo['liveStreamingDetails']['scheduledStartTime']
    Planed_Start_Time=APItimeSetToUTC8(Planed_Start_Time)
else:
    Planed_Start_Time='NaN'

if "actualStartTime" in sinfo['liveStreamingDetails']:
    Actual_Start_Time=sinfo['liveStreamingDetails']['actualStartTime']
    Actual_Start_Time=APItimeSetToUTC8(Actual_Start_Time)

#檢查直播是否開始
liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']

notStartHold = sleep_time(0, 1, 0)
while liveBroadcastContent=='none':
    print('直播已結束')
    break
while liveBroadcastContent=='upcoming':
    try:
        localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
        localtime=localTimeClean(localtime)
        print(localtime+'(UTC+8) 直播尚未開始,等待一分鐘後自動重新確認')
        time.sleep(notStartHold)
        sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
        liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']
    except KeyboardInterrupt:
        print('---在等待直播開始時手動跳出,接下來的執行會出問題---')
        break
    except:
        continue
    if liveBroadcastContent == 'live':
        break

Title=sinfo['snippet']['title']
TitleFileName=re.sub('[\/:*?"<>|]',' ',Title)
Actual_Start_Time=sinfo['liveStreamingDetails']['actualStartTime']
Actual_Start_Time=APItimeSetToUTC8(Actual_Start_Time)

ActualStartTimeFileName=datetime.datetime.strftime(Actual_Start_Time,'%Y-%m-%d %H:%M:%S ')
ActualStartTimeFileName=ActualStartTimeFileName[0:10]

if os.path.isdir(ActualStartTimeFileName+' '+TitleFileName):
    os.chdir(ActualStartTimeFileName+' '+TitleFileName)
else:
    os.mkdir(ActualStartTimeFileName+' '+TitleFileName)
    os.chdir(ActualStartTimeFileName+' '+TitleFileName)

#開啟csv檔寫入直播數據
streamData=open(TitleFileName+'.csv', 'a', newline='', encoding='UTF-8')
#streamData.write('time,concurrentViewers,viewCount,likeCount,dislikeCount\n')

#開啟txt檔寫入直播資訊
streamInfo=open('info of '+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8')
streamInfoCollectstart=['頻道 Channel:',Channel,'\n','標題 Title:',Title,'\n','影片ID Video_ID:',Video_ID,'\n','直播公開時間 Stream Created time(UTC+8):',str(Stream_Created),'\n','預定開始時間 Planed Start Time(UTC+8):',str(Planed_Start_Time),'\n']
streamInfo.writelines(streamInfoCollectstart)

streamInfoCollectAST=['實際開始時間 Actual Start Time(UTC+8):',str(Actual_Start_Time),'\n']
streamInfo.writelines(streamInfoCollectAST)
Log_Start_Time = datetime.datetime.now().replace(microsecond=0).isoformat()
Log_Start_Time=localTimeClean(Log_Start_Time)
streamInfo.write('紀錄開始時間 Log Start Time(UTC+8):'+Log_Start_Time+'\n')

#直播開始後寫入csv
while liveBroadcastContent=='live':

    try:
        localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
        localtime=localTimeClean(localtime)
        if liveBroadcastContent != 'live':
            break
        sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
        liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']

        if "concurrentViewers" in sinfo['liveStreamingDetails']:
            concurrentViewers=sinfo['liveStreamingDetails']['concurrentViewers']
        else:
            concurrentViewers=0
        
        if "viewCount" in sinfo['statistics']:
            viewCount=sinfo['statistics']['viewCount']
        else:
            viewCount=0

        if "likeCount" in sinfo['statistics']:
            likeCount=sinfo['statistics']['likeCount']
        else:
            likeCount=0

        if "dislikeCount" in sinfo['statistics']:
            dislikeCount=sinfo['statistics']['dislikeCount']
        else:
            dislikeCount=0

        streamData.write(str(localtime)+','+str(concurrentViewers)+','+str(viewCount)+','+str(likeCount)+','+str(dislikeCount)+'\n')
        print(str(localtime)+','+str(concurrentViewers)+','+str(viewCount)+','+str(likeCount)+','+str(dislikeCount))
        
        second = sleep_time(0, 0, 9)
        time.sleep(second)
    except KeyboardInterrupt:
        logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
        logStopTime=localTimeClean(logStopTime)
        print('---手動跳出紀錄---')
        break
    except:
        continue

streamData.close()
#找同接最大值
headers=['time','concurrentViewers','viewCount','likeCount','dislikeCount']
df = pd.read_csv(TitleFileName+'.csv', names=headers,header=None,usecols=[0,1,2,3,4])
#csvRead=pd.read_csv(TitleFileName+'.csv')
MaxConcurrentViewers=df['concurrentViewers'].max()

logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
logStopTime=localTimeClean(logStopTime)
#info寫入
if "actualEndTime" in sinfo['liveStreamingDetails']:
    Actual_End_Time=sinfo['liveStreamingDetails']['actualEndTime']
    Actual_End_Time=APItimeSetToUTC8(Actual_End_Time)
    streamInfo.write('直播結束時間 Actual End Time(UTC+8):'+str(Actual_End_Time)+'\n')
else:
    Actual_End_Time='NaN'
    streamInfo.write('直播結束時間 Actual End Time(UTC+8):NaN\n')

streamInfo.write('紀錄結束時間 Log stop Time(UTC+8):'+str(logStopTime)+'\n')

streamInfo.write('紀錄結束時最高同時觀看人數 Max Concurrent Viewers:'+str(MaxConcurrentViewers)+'\n')

if "viewCount" in sinfo['statistics']:
    streamInfo.write('紀錄結束時播放數 View Count:'+str(viewCount)+'\n')
else:
    streamInfo.write('紀錄結束時播放數 View Count:NaN'+'\n')

if "likeCount" in sinfo['statistics']:
    streamInfo.write('紀錄結束時喜歡數 Like Count:'+str(likeCount)+'\n')
else:
    streamInfo.write('紀錄結束時喜歡數 Like Count:NaN'+'\n')

if "dislikeCount" in sinfo['statistics']:
    streamInfo.write('紀錄結束時不喜歡數 Dislike Count:'+str(dislikeCount)+'\n')
else:
    streamInfo.write('紀錄結束時不喜歡數 Dislike Count:NaN'+'\n')

streamInfo.close()


#繪圖
chartTitle='Channel: '+Channel+'\n'+'Title: '+Title+'\n'

#這裡應該能簡化

t = df['time']
c = df['concurrentViewers']
v = df['viewCount']
l = df['likeCount']
d = df['dislikeCount']

MaxConcurrentViewers=df['concurrentViewers'].max()
MaxViewCount=df['viewCount'].max()
MaxLikeCount=df['likeCount'].max()
MaxDislikeCount=df['dislikeCount'].max()
countResult='MaxConcurrentViewers:{0}\nMaxLikeCount:{1}\nMaxDislikeCount:{2}\nMaxViewCount:{3}'.format(MaxConcurrentViewers,MaxLikeCount,MaxDislikeCount,MaxViewCount)
timeResult='Planed Start Time(UTC+8):{0}\nActual Start Time(UTC+8):{1}\nLog Start Time(UTC+8):{2}\nActual End Time(UTC+8):{3}'.format(Planed_Start_Time,Actual_Start_Time,Log_Start_Time,Actual_End_Time)

#標題副標題,圖表結構,部分頻道和標題因字型問題無法完整顯示
fig, (ax1, ax2) = plt.subplots(2,sharex=True,figsize=(12.8,7.2))
fig.suptitle(chartTitle,fontname="MS Gothic", fontsize=15)
fig.set_facecolor('lightgray')
ax1.set_facecolor('gainsboro')
ax1.set_title(countResult,loc='left', fontsize=12)
ax1.set_title(timeResult,loc='right', fontsize=12)

#圖表1
ax1.set_ylabel('count')
ax1.plot(t,c,'b',label='concurrentViewers')
ax1.plot(t,l,'g',label='likeCount')
ax1.plot(t,d,'r',label='dislikeCount')
ax1.legend(loc='upper left')
ax1.ticklabel_format(axis='y', style='plain')
ax1.grid(True)

#圖表2
ax2.set_facecolor('gainsboro')
ax2.plot(t,v,'c',label='viewCount')
ax2.legend(loc='upper left')
#ax2.set_ylim(0,MaxViewCount)
ax2.ticklabel_format(axis='y', style='plain')
ax2.set_ylabel('count')
ax2.grid(True)

#X軸簡化
x = df.time
ticker_spacing = x
ticker_spacing = 160
ax2.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
plt.xticks(rotation=20, fontsize=7)
plt.xlabel('time')

#儲存圖表
fig.tight_layout()
print('---儲存折線圖---')
plt.savefig('chart of ' + TitleFileName + '.png')
print('---儲存完成---')

#結束後輸出
print('頻道 Channel:', sinfo['snippet']['channelTitle'])
print('標題 Title:', sinfo['snippet']['title'])
print('影片ID Video ID:', sinfo['id'])
if "publishedAt" in sinfo['snippet']:
    print('直播公開時間 Stream Created Time(UTC+8):', Stream_Created)
else:
    print('直播公開時間 Stream Created Time(UTC+8):NaN')

if "scheduledStartTime" in sinfo['liveStreamingDetails']:
    print('預定開始時間 Planed Start Time(UTC+8):', Planed_Start_Time)
else:
    print('預定開始時間 Planed Start Time(UTC+8):NaN')

if "actualStartTime" in sinfo['liveStreamingDetails']:
    print('實際開始時間 Actual Start Time(UTC+8):', Actual_Start_Time)
else:
    print('實際開始時間 Actual Start Time(UTC+8):NaN')

if "actualEndTime" in sinfo['liveStreamingDetails']:
    print('直播結束時間 Actual End Time(UTC+8):', Actual_End_Time)
else:
    print('直播結束時間 Actual End Time(UTC+8):NaN\n')

print('紀錄結束時間 Log Stop Time(UTC+8): '+str(logStopTime))

#print('是否在直播 liveBroadcastContent:', sinfo['snippet']['liveBroadcastContent'])
'''
if "concurrentViewers" in sinfo['liveStreamingDetails']:
    print('同時觀看人數 concurrentViewers:', sinfo['liveStreamingDetails']['concurrentViewers'])
else:
    print('同時觀看人數 concurrentViewers:NaN')
'''

print('紀錄結束時最高同時觀看人數 Max Concurrent Viewers: '+str(MaxConcurrentViewers))

if "viewCount" in sinfo['statistics']:
    print('紀錄結束時播放數 View Count:', sinfo['statistics']['viewCount'])
else:
    print('紀錄結束時播放數 View Count:NaN')

if "likeCount" in sinfo['statistics']:
    print('紀錄結束時喜歡數 Like Count:', sinfo['statistics']['likeCount'])
else:
    print('紀錄結束時喜歡數 Like Count:NaN')

if "dislikeCount" in sinfo['statistics']:
    print('紀錄結束時不喜歡數 Dislike Count:', sinfo['statistics']['dislikeCount'])
else:
    print('紀錄結束時不喜歡數 DislikeCount:NaN')

#開啟csv檔寫入直播後數據
countAfterStream=open('count after stream of '+TitleFileName+'.csv', 'a', newline='', encoding='UTF-8')
#countAfterStream.write('time,viewCount,likeCount,dislikeCount\n')

#開啟txt檔寫入直播後資訊
countInfo=open('count after stream info of '+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8')
streamInfoCollectstart=['count after stream: 1 day version\n','頻道 Channel:',Channel,'\n','標題 Title:',Title,'\n','影片ID Video_ID:',Video_ID,'\n','直播公開時間 Stream Created time(UTC+8):',str(Stream_Created),'\n','預定開始時間 Planed Start Time(UTC+8):',str(Planed_Start_Time),'\n']
countInfo.writelines(streamInfoCollectstart)

streamInfoCollectAST=['實際開始時間 Actual Start Time(UTC+8):',str(Actual_Start_Time),'\n']
countInfo.writelines(streamInfoCollectAST)
Log_Start_Time = datetime.datetime.now().replace(microsecond=0).isoformat()
Log_Start_Time=localTimeClean(Log_Start_Time)
countInfo.write('紀錄開始時間 Log Start Time(UTC+8):'+Log_Start_Time+'\n')

#寫入csv,預設一天,144*10min

for i in range(144):

    try:
        localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
        localtime=localTimeClean(localtime)

        sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)

        if "viewCount" in sinfo['statistics']:
            viewCount=sinfo['statistics']['viewCount']
        else:
            viewCount=0

        if "likeCount" in sinfo['statistics']:
            likeCount=sinfo['statistics']['likeCount']
        else:
            likeCount=0

        if "dislikeCount" in sinfo['statistics']:
            dislikeCount=sinfo['statistics']['dislikeCount']
        else:
            dislikeCount=0
        
        if "commentCount" in sinfo['statistics']:
            commentCount=sinfo['statistics']['commentCount']
        else:
            commentCount=0

        countAfterStream.write(str(localtime)+','+str(viewCount)+','+str(likeCount)+','+str(dislikeCount)+','+str(commentCount)+'\n')
        print(str(localtime)+','+str(viewCount)+','+str(likeCount)+','+str(dislikeCount)+','+str(commentCount))
        
        second = sleep_time(0, 10, 0)
        time.sleep(second)
    except KeyboardInterrupt:
        logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
        logStopTime=localTimeClean(logStopTime)
        print('---手動跳出紀錄---')
        break
    except:
        continue

countAfterStream.close()

logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
logStopTime=localTimeClean(logStopTime)
#info寫入
if "actualEndTime" in sinfo['liveStreamingDetails']:
    Actual_End_Time=sinfo['liveStreamingDetails']['actualEndTime']
    Actual_End_Time=APItimeSetToUTC8(Actual_End_Time)
    countInfo.write('直播結束時間 Actual End Time(UTC+8):'+str(Actual_End_Time)+'\n')
else:
    Actual_End_Time='NaN'
    countInfo.write('直播結束時間 Actual End Time(UTC+8):NaN\n')

countInfo.write('紀錄結束時間 Log stop Time(UTC+8):'+str(logStopTime)+'\n')

if "viewCount" in sinfo['statistics']:
    countInfo.write('紀錄結束時播放數 View Count:'+str(viewCount)+'\n')
else:
    countInfo.write('紀錄結束時播放數 View Count:NaN'+'\n')

if "likeCount" in sinfo['statistics']:
    countInfo.write('紀錄結束時喜歡數 Like Count:'+str(likeCount)+'\n')
else:
    countInfo.write('紀錄結束時喜歡數 Like Count:NaN'+'\n')

if "dislikeCount" in sinfo['statistics']:
    countInfo.write('紀錄結束時不喜歡數 Dislike Count:'+str(dislikeCount)+'\n')
else:
    countInfo.write('紀錄結束時不喜歡數 Dislike Count:NaN'+'\n')

if "commentCount" in sinfo['statistics']:
    countInfo.write('紀錄結束時留言數 Comment Count:'+str(commentCount)+'\n')
else:
    countInfo.write('紀錄結束時留言數 Comment Count:NaN'+'\n')

countInfo.close()


#繪圖
chartTitle='Channel: '+Channel+'\n'+'Title: '+Title+'\n'+'Count after stream'

#這裡應該能簡化
headers=['time','viewCount','likeCount','dislikeCount','commentCount']
dfafter = pd.read_csv('count after stream of '+TitleFileName+'.csv', names=headers,header=None,usecols=[0,1,2,3,4])

t = dfafter['time']

v = dfafter['viewCount']
l = dfafter['likeCount']
d = dfafter['dislikeCount']
c = dfafter['commentCount']

MaxViewCount=dfafter['viewCount'].max()
MaxLikeCount=dfafter['likeCount'].max()
MaxDislikeCount=dfafter['dislikeCount'].max()
MaxCommentCount=dfafter['commentCount'].max()
countResult='MaxLikeCount:{0}\nMaxDislikeCount:{1}\nMaxViewCount:{2}\nMaxCommentCount:{3}'.format(MaxLikeCount,MaxDislikeCount,MaxViewCount,MaxCommentCount)
timeResult='Actual Start Time(UTC+8):{0}\nActual End Time(UTC+8):{1}\nLog Start Time(UTC+8):{2}\nLog Stop Time(UTC+8):{3}'.format(Actual_Start_Time,Actual_End_Time,Log_Start_Time,logStopTime)

#標題副標題,圖表結構,部分頻道和標題因字型問題無法完整顯示
fig2, (ax3, ax4, ax5) = plt.subplots(3,sharex=True,figsize=(12.8,10.8))
fig2.suptitle(chartTitle,fontname="MS Gothic", fontsize=15)
fig2.set_facecolor('paleturquoise')
ax3.set_facecolor('lightcyan')
ax3.set_title(countResult,loc='left', fontsize=12)
ax3.set_title(timeResult,loc='right', fontsize=12)

#圖表1
ax3.set_ylabel('count')

ax3.plot(t,l,'g',label='likeCount')
ax3.plot(t,d,'r',label='dislikeCount')
ax3.legend(loc='upper left')
ax3.ticklabel_format(axis='y', style='plain')
ax3.grid(True)

#圖表2
ax4.set_facecolor('lightcyan')
ax4.plot(t,v,'c',label='viewCount')
ax4.legend(loc='upper left')
ax4.ticklabel_format(axis='y', style='plain')
ax4.set_ylabel('count')
ax4.grid(True)

#圖表3
ax5.set_facecolor('lightcyan')
ax5.plot(t,c,'darkcyan',label='commentCount')
ax5.legend(loc='upper left')
ax5.ticklabel_format(axis='y', style='plain')
ax5.set_ylabel('count')
ax5.grid(True)

#X軸簡化
x = dfafter.time
ticker_spacing = x
ticker_spacing = 6
ax5.xaxis.set_major_locator(ticker.MultipleLocator(ticker_spacing))
plt.xticks(rotation=20, fontsize=7)
plt.xlabel('time')

#儲存圖表
fig2.tight_layout()
print('---儲存折線圖---')
plt.savefig('count chart after stream of ' + TitleFileName + '.png')
print('---儲存完成---')

#結束後輸出
print('頻道 Channel:', sinfo['snippet']['channelTitle'])
print('標題 Title:', sinfo['snippet']['title'])
print('影片ID Video ID:', sinfo['id'])
if "publishedAt" in sinfo['snippet']:
    print('直播公開時間 Stream Created Time(UTC+8):', Stream_Created)
else:
    print('直播公開時間 Stream Created Time(UTC+8):NaN')

if "scheduledStartTime" in sinfo['liveStreamingDetails']:
    print('預定開始時間 Planed Start Time(UTC+8):', Planed_Start_Time)
else:
    print('預定開始時間 Planed Start Time(UTC+8):NaN')

if "actualStartTime" in sinfo['liveStreamingDetails']:
    print('實際開始時間 Actual Start Time(UTC+8):', Actual_Start_Time)
else:
    print('實際開始時間 Actual Start Time(UTC+8):NaN')

if "actualEndTime" in sinfo['liveStreamingDetails']:
    print('直播結束時間 Actual End Time(UTC+8):', Actual_End_Time)
else:
    print('直播結束時間 Actual End Time(UTC+8):NaN\n')


print('紀錄結束時間 Log Stop Time(UTC+8): '+str(logStopTime))

if "viewCount" in sinfo['statistics']:
    print('紀錄結束時播放數 View Count:', sinfo['statistics']['viewCount'])
else:
    print('紀錄結束時播放數 View Count:NaN')

if "likeCount" in sinfo['statistics']:
    print('紀錄結束時喜歡數 Like Count:', sinfo['statistics']['likeCount'])
else:
    print('紀錄結束時喜歡數 Like Count:NaN')

if "dislikeCount" in sinfo['statistics']:
    print('紀錄結束時不喜歡數 Dislike Count:', sinfo['statistics']['dislikeCount'])
else:
    print('紀錄結束時不喜歡數 Dislike Count:NaN')

if "commentCount" in sinfo['statistics']:
    print('紀錄結束時留言數 Comment Count:', sinfo['statistics']['commentCount'])
else:
    print('紀錄結束時留言數 Comment Count:NaN')
