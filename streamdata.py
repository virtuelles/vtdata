# coding=utf-8
from datetime import *
import pandas as pd
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
     Use "videos" function to derive info of livestream
    '''
    params = {
              'part': 'liveStreamingDetails,statistics,snippet',
              'key': API_KEY,
              'id': vID,
              'fields': 'items(id,liveStreamingDetails(activeLiveChatId,concurrentViewers,scheduledStartTime,actualStartTime,actualEndTime),' + 
              'snippet(channelId,channelTitle,description,liveBroadcastContent,publishedAt,thumbnails,title),statistics)'
              }
    headers = {'User-Agent': 'Chrome/92.0.4515.107'}
    url = 'https://www.googleapis.com/youtube/v3/videos'
    req = requests.get(url, headers=headers, params=params).json()
    
    streamData = dict(req.get('items')[0])
    
    return streamData

localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
localtime=localTimeClean(localtime)
print('紀錄開始時間start at(UTC+8): '+localtime)

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

notStartHold = sleep_time(0, 0, 30)
while liveBroadcastContent=='none':
    print('直播已結束')
    break
while liveBroadcastContent=='upcoming':
    localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
    localtime=localTimeClean(localtime)
    print(localtime+'(UTC+8) 直播尚未開始,等待30秒後自動重新確認')
    time.sleep(notStartHold)
    sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
    liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']
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
streamData.write('time,concurrentViewers,viewCount,likeCount,dislikeCount\n')

#開啟txt檔寫入直播資訊
streamInfo=open('info of '+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8')
streamInfoCollectstart=['頻道 Channel:',Channel,'\n','標題 Title:',Title,'\n','影片ID Video_ID:',Video_ID,'\n','直播公開時間 Stream Created time(UTC+8):',str(Stream_Created),'\n','預定開始時間 Planed Start Time(UTC+8):',str(Planed_Start_Time),'\n']
streamInfo.writelines(streamInfoCollectstart)

streamInfoCollectAST=['實際開始時間 Actual Start Time(UTC+8):',str(Actual_Start_Time),'\n']
streamInfo.writelines(streamInfoCollectAST)
localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
localtime=localTimeClean(localtime)
streamInfo.write('紀錄開始時間 Log Start Time(UTC+8):'+localtime+'\n')

#直播開始後寫入csv
while liveBroadcastContent=='live':

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
streamData.close()
#找同接最大值
csvRead=pd.read_csv(TitleFileName+'.csv')
MaxConcurrentViewers=csvRead['concurrentViewers'].max()

#info寫入
if "actualEndTime" in sinfo['liveStreamingDetails']:
    actualEndTime=sinfo['liveStreamingDetails']['actualEndTime']
    actualEndTime=APItimeSetToUTC8(actualEndTime)
    streamInfo.write('直播結束時間 Actual End Time(UTC+8):'+str(actualEndTime)+'\n')

streamInfo.write('最高同時觀看人數 Max Concurrent Viewers:'+str(MaxConcurrentViewers)+'\n')

if "viewCount" in sinfo['statistics']:
    streamInfo.write('結束時播放數 View Count:'+str(viewCount)+'\n')
else:
    streamInfo.write('結束時播放數 View Count:NaN'+'\n')

if "likeCount" in sinfo['statistics']:
    streamInfo.write('結束時喜歡數 Like Count:'+str(likeCount)+'\n')
else:
    streamInfo.write('結束時喜歡數 Like Count:NaN'+'\n')

if "dislikeCount" in sinfo['statistics']:
    streamInfo.write('結束時不喜歡數 Dislike Count:'+str(dislikeCount)+'\n')
else:
    streamInfo.write('結束時不喜歡數 Dislike Count:NaN'+'\n')







streamInfo.close()
#結束後輸出
print('頻道 Channel:', sinfo['snippet']['channelTitle'])
print('標題 Title:', sinfo['snippet']['title'])
print('影片ID Video ID:', sinfo['id'])
if "publishedAt" in sinfo['snippet']:
    print('直播公開時間 Stream Created Time(UTC+8):', Stream_Created)

if "scheduledStartTime" in sinfo['liveStreamingDetails']:
    print('預定開始時間 Planed Start Time(UTC+8):', Planed_Start_Time)

if "actualStartTime" in sinfo['liveStreamingDetails']:
    print('實際開始時間 Actual Start Time(UTC+8):', Actual_Start_Time)

if "actualEndTime" in sinfo['liveStreamingDetails']:
    print('直播結束時間 Actual End Time(UTC+8):', actualEndTime)

#print('是否在直播 liveBroadcastContent:', sinfo['snippet']['liveBroadcastContent'])
'''
if "concurrentViewers" in sinfo['liveStreamingDetails']:
    print('同時觀看人數 concurrentViewers:', sinfo['liveStreamingDetails']['concurrentViewers'])
else:
    print('同時觀看人數 concurrentViewers:NaN')
'''

print('最高同時觀看人數 Max Concurrent Viewers: '+str(MaxConcurrentViewers))

if "viewCount" in sinfo['statistics']:
    print('結束時播放數 View Count:', sinfo['statistics']['viewCount'])
else:
    print('結束時播放數 View Count:NaN')

if "likeCount" in sinfo['statistics']:
    print('結束時喜歡數 Like Count:', sinfo['statistics']['likeCount'])
else:
    print('結束時喜歡數 Like Count:NaN')

if "dislikeCount" in sinfo['statistics']:
    print('結束時不喜歡數 Dislike Count:', sinfo['statistics']['dislikeCount'])
else:
    print('結束時不喜歡數 DislikeCount:NaN')
