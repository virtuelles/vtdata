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
    Use "videos" function to derive info of livestream
    '''
    params = {
            'part': 'liveStreamingDetails,statistics,snippet',
            'key': API_KEY,
            'id': vID,
            'fields': 'items(id,snippet(publishedAt,channelId,title,channelTitle,,liveBroadcastContent),statistics,liveStreamingDetails)'
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

try:
    if "scheduledStartTime" in sinfo['liveStreamingDetails']:
        Planed_Start_Time=sinfo['liveStreamingDetails']['scheduledStartTime']
        Planed_Start_Time=APItimeSetToUTC8(Planed_Start_Time)
    else:
        Planed_Start_Time='NaN'

    if "actualStartTime" in sinfo['liveStreamingDetails']:
        Actual_Start_Time=sinfo['liveStreamingDetails']['actualStartTime']
        Actual_Start_Time=APItimeSetToUTC8(Actual_Start_Time)
except:
    Planed_Start_Time='NaN'
    Actual_Start_Time='NaN'

#檢查直播是否開始
liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']

notStartHold = sleep_time(0, 1, 0)
while liveBroadcastContent=='none':
    Title=sinfo['snippet']['title']
    print('直播已結束')
    print('Channel: ',Channel)
    print('Tilte: ',Title)
    break
while liveBroadcastContent=='upcoming':
    try:
        localtime = datetime.datetime.now().replace(microsecond=0).isoformat()
        localtime = localTimeClean(localtime)
        localtime = datetime.datetime.strptime(localtime,"%Y-%m-%d %H:%M:%S")
        if "scheduledStartTime" in sinfo['liveStreamingDetails']:
            Planed_Start_Time=sinfo['liveStreamingDetails']['scheduledStartTime']
            Planed_Start_Time=APItimeSetToUTC8(Planed_Start_Time)
        else:
            Planed_Start_Time='NaN'
        #print(localtime)
        #print(Planed_Start_Time)
        delta = Planed_Start_Time - localtime
        Title=sinfo['snippet']['title']

        print('Channel: ',Channel)
        print('Tilte: ',Title)
        print('剩餘多少時間開始: ',delta.total_seconds(),'秒')
        
        if delta.total_seconds() >0:
            print('現在時間: ',str(localtime),'(UTC+8) 直播於', delta ,'後開始,','將等待', delta )
            time.sleep(delta.total_seconds())
        else:
            print('現在時間: ',str(localtime),'(UTC+8) 直播尚未開始,等待一分鐘後檢查')
            time.sleep(notStartHold)
        sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
        liveBroadcastContent=sinfo['snippet']['liveBroadcastContent']
        if liveBroadcastContent == 'live':
            break
    except KeyboardInterrupt:
        print('---在等待直播開始時手動跳出,接下來的執行會出問題---')
        break
    except:
        print('八成出了bug')
        notStartHold = sleep_time(0, 1, 0)
        time.sleep(notStartHold)
        continue

Title=sinfo['snippet']['title']
TitleFileName=re.sub('[\/:*?"<>|]',' ',Title)
try:
    Actual_Start_Time=sinfo['liveStreamingDetails']['actualStartTime']
    Actual_Start_Time=APItimeSetToUTC8(Actual_Start_Time)

    ActualStartTimeFileName=datetime.datetime.strftime(Actual_Start_Time,'%Y-%m-%d %H:%M:%S ')
    ActualStartTimeFileName=ActualStartTimeFileName[0:10]
except:
    Actual_Start_Time='NaN'
    ActualStartTimeFileName=datetime.datetime.strftime(Stream_Created,'%Y-%m-%d %H:%M:%S ')
    ActualStartTimeFileName=ActualStartTimeFileName[0:10]

if os.path.isdir(ActualStartTimeFileName+' '+TitleFileName):
    os.chdir(ActualStartTimeFileName+' '+TitleFileName)
else:
    os.mkdir(ActualStartTimeFileName+' '+TitleFileName)
    os.chdir(ActualStartTimeFileName+' '+TitleFileName)

#開啟txt檔寫入直播資訊
with open('SI_'+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8') as streamInfo:
    streamInfoCollectstart=['Video_ID:',Video_ID,'\n','Stream Created time(UTC+8):',str(Stream_Created),'\n','Planed Start Time(UTC+8):',str(Planed_Start_Time),'\n']
    streamInfo.writelines(streamInfoCollectstart)

    streamInfoCollectAST=['Actual Start Time(UTC+8):',str(Actual_Start_Time),'\n']
    streamInfo.writelines(streamInfoCollectAST)
    Log_Start_Time = datetime.datetime.now().replace(microsecond=0).isoformat()
    Log_Start_Time=localTimeClean(Log_Start_Time)
    streamInfo.write('Log Start Time(UTC+8):'+Log_Start_Time+'\n')
#開啟csv檔寫入直播數據
with open('SD_'+TitleFileName+'.csv', 'a', newline='', encoding='UTF-8') as streamData:
    #streamData.write('time,concurrentViewers,viewCount,likeCount,dislikeCount\n')

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

            '''if "dislikeCount" in sinfo['statistics']:
                dislikeCount=sinfo['statistics']['dislikeCount']
            else:
                dislikeCount=0'''

            streamData.write(str(localtime)+','+str(concurrentViewers)+','+str(viewCount)+','+str(likeCount)+'\n')
            print(str(localtime)+','+str(concurrentViewers)+','+str(viewCount)+','+str(likeCount))
            
            second = sleep_time(0, 0, 9)
            time.sleep(second)
        except KeyboardInterrupt:
            logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
            logStopTime=localTimeClean(logStopTime)
            print('---手動跳出紀錄---')
            break
        except:
            print('可能連線錯誤')
            second = sleep_time(0, 0, 9)
            time.sleep(second)
            continue
#找同接最大值
headers=['time','concurrentViewers','viewCount','likeCount']
df = pd.read_csv('SD_'+TitleFileName+'.csv', names=headers,header=None,usecols=[0,1,2,3])
#csvRead=pd.read_csv(TitleFileName+'.csv')
MaxConcurrentViewers=df['concurrentViewers'].max()

logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
logStopTime=localTimeClean(logStopTime)
#info寫入
with open('SI_'+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8') as streamInfo:
    if "actualEndTime" in sinfo['liveStreamingDetails']:
        Actual_End_Time=sinfo['liveStreamingDetails']['actualEndTime']
        Actual_End_Time=APItimeSetToUTC8(Actual_End_Time)
        streamInfo.write('Actual End Time(UTC+8):'+str(Actual_End_Time)+'\n')
    else:
        Actual_End_Time='NaN'
        streamInfo.write('Actual End Time(UTC+8):NaN\n')

    streamInfo.write('Log stop Time(UTC+8):'+str(logStopTime)+'\n')

    sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
    Title=sinfo['snippet']['title']
    streamInfo.write('Channel:'+str(Channel)+'\n')
    streamInfo.write('Title:'+str(Title)+'\n')

    streamInfo.write('Max Concurrent Viewers:'+str(MaxConcurrentViewers)+'\n')

    if "viewCount" in sinfo['statistics']:
        streamInfo.write('View Count:'+str(viewCount)+'\n')
    else:
        streamInfo.write('View Count:NaN'+'\n')

    if "likeCount" in sinfo['statistics']:
        streamInfo.write('Like Count:'+str(likeCount)+'\n')
    else:
        streamInfo.write('Like Count:NaN'+'\n')

    '''if "dislikeCount" in sinfo['statistics']:
        streamInfo.write('Dislike Count:'+str(dislikeCount)+'\n')
    else:
        streamInfo.write('Dislike Count(R.I.P):NaN'+'\n')'''

#繪圖
chartTitle='Channel: '+Channel+'\n'+'Title: '+Title+'\n'

#這裡應該能簡化

t = df['time']
c = df['concurrentViewers']
v = df['viewCount']
l = df['likeCount']
#d = df['dislikeCount']

MaxConcurrentViewers=df['concurrentViewers'].max()
MaxViewCount=df['viewCount'].max()
MaxLikeCount=df['likeCount'].max()
#MaxDislikeCount=df['dislikeCount'].max()
countResult='MaxConcurrentViewers:{0}\nMaxLikeCount:{1}\nMaxViewCount:{2}'.format(MaxConcurrentViewers,MaxLikeCount,MaxViewCount)
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
#ax1.plot(t,d,'r',label='dislikeCount')
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
plt.savefig('SC_' + TitleFileName + '.png')
print('---儲存完成---')

#結束後輸出
print('Channel:', sinfo['snippet']['channelTitle'])
print('Title:', sinfo['snippet']['title'])
print('Video ID:', sinfo['id'])
if "publishedAt" in sinfo['snippet']:
    print('Stream Created Time(UTC+8):', Stream_Created)
else:
    print('Stream Created Time(UTC+8):NaN')

if "scheduledStartTime" in sinfo['liveStreamingDetails']:
    print('Planed Start Time(UTC+8):', Planed_Start_Time)
else:
    print('Planed Start Time(UTC+8):NaN')

if "actualStartTime" in sinfo['liveStreamingDetails']:
    print('Actual Start Time(UTC+8):', Actual_Start_Time)
else:
    print('Actual Start Time(UTC+8):NaN')

if "actualEndTime" in sinfo['liveStreamingDetails']:
    print('Actual End Time(UTC+8):', Actual_End_Time)
else:
    print('Actual End Time(UTC+8):NaN')

print('Log Stop Time(UTC+8): '+str(logStopTime))

#print('是否在直播 liveBroadcastContent:', sinfo['snippet']['liveBroadcastContent'])
'''
if "concurrentViewers" in sinfo['liveStreamingDetails']:
    print('同時觀看人數 concurrentViewers:', sinfo['liveStreamingDetails']['concurrentViewers'])
else:
    print('同時觀看人數 concurrentViewers:NaN')
'''

print('Max Concurrent Viewers: '+str(MaxConcurrentViewers))

if "viewCount" in sinfo['statistics']:
    print('View Count:', sinfo['statistics']['viewCount'])
else:
    print('View Count:NaN')

if "likeCount" in sinfo['statistics']:
    print('Like Count:', sinfo['statistics']['likeCount'])
else:
    print('Like Count:NaN')

'''if "dislikeCount" in sinfo['statistics']:
    print('Dislike Count:', sinfo['statistics']['dislikeCount'])
else:
    print('DislikeCount:NaN')'''

print('~~~直播記錄結束,直播後記錄開始~~~')

with open('CASI_'+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8') as countInfo:
    streamInfoCollectstart=['count for 1 day\n','Video_ID:',Video_ID,'\n','Stream Created time(UTC+8):',str(Stream_Created),'\n','Planed Start Time(UTC+8):',str(Planed_Start_Time),'\n']
    countInfo.writelines(streamInfoCollectstart)

    streamInfoCollectAST=['Actual Start Time(UTC+8):',str(Actual_Start_Time),'\n']
    countInfo.writelines(streamInfoCollectAST)
    Log_Start_Time = datetime.datetime.now().replace(microsecond=0).isoformat()
    Log_Start_Time=localTimeClean(Log_Start_Time)
    countInfo.write('Log Start Time(UTC+8):'+Log_Start_Time+'\n')
#開啟csv檔寫入直播後數據
with open('CAS_'+TitleFileName+'.csv', 'a', newline='', encoding='UTF-8') as countAfterStream:
    #countAfterStream.write('time,viewCount,likeCount,dislikeCount\n')

    #開啟txt檔寫入直播後資訊

    #寫入csv,預設一天,144*10min

    viewCount150min=0
    likeCount150min=0
    #dislikeCount150min=0
    commentCount150min=0
    viewCount180min=0
    likeCount180min=0
    #dislikeCount180min=0
    commentCount180min=0

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

            '''if "dislikeCount" in sinfo['statistics']:
                dislikeCount=sinfo['statistics']['dislikeCount']
            else:
                dislikeCount=0'''
            
            if "commentCount" in sinfo['statistics']:
                commentCount=sinfo['statistics']['commentCount']
            else:
                commentCount=0
            
            if i == 14:
                viewCount150min=viewCount
                likeCount150min=likeCount
                #dislikeCount150min=dislikeCount
                commentCount150min=commentCount
            if i == 17:
                viewCount180min=viewCount
                likeCount180min=likeCount
                #dislikeCount180min=dislikeCount
                commentCount180min=commentCount

            countAfterStream.write(str(localtime)+','+str(viewCount)+','+str(likeCount)+','+str(commentCount)+'\n')
            print(str(localtime)+','+str(viewCount)+','+str(likeCount)+','+str(commentCount))
            
            second = sleep_time(0, 10, 0)
            time.sleep(second)

        except KeyboardInterrupt:
            logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
            logStopTime=localTimeClean(logStopTime)
            print('---手動跳出紀錄---')
            break
        except:
            second = sleep_time(0, 10, 0)
            time.sleep(second)
            continue

logStopTime = datetime.datetime.now().replace(microsecond=0).isoformat()
logStopTime=localTimeClean(logStopTime)
#info寫入
with open('CASI_'+TitleFileName+'.txt', 'a', newline='', encoding='UTF-8') as countInfo:
    try:
        if "actualEndTime" in sinfo['liveStreamingDetails']:
            Actual_End_Time=sinfo['liveStreamingDetails']['actualEndTime']
            Actual_End_Time=APItimeSetToUTC8(Actual_End_Time)
            countInfo.write('Actual End Time(UTC+8):'+str(Actual_End_Time)+'\n')
        else:
            Actual_End_Time='NaN'
            countInfo.write('Actual End Time(UTC+8):NaN\n')
    except:
        Actual_End_Time='NaN'
        countInfo.write('Actual End Time(UTC+8):NaN\n')

    countInfo.write('Log stop Time(UTC+8):'+str(logStopTime)+'\n')

    sinfo = get_livestream_info(API_KEY[apiKeySelect],vid)
    Title=sinfo['snippet']['title']
    countInfo.write('Channel:'+str(Channel)+'\n')
    countInfo.write('Title:'+str(Title)+'\n')

    countInfo.write('View Count at 2.5hr:'+str(viewCount150min)+'\n')
    countInfo.write('Like Count at 2.5hr:'+str(likeCount150min)+'\n')
    #countInfo.write('Dislike Count at 2.5hr:'+str(dislikeCount150min)+'\n')
    countInfo.write('Comment Count at 2.5hr:'+str(commentCount150min)+'\n')

    countInfo.write('View Count at 3hr:'+str(viewCount180min)+'\n')
    countInfo.write('Like Count at 3hr:'+str(likeCount180min)+'\n')
    #countInfo.write('Dislike Count at 3hr:'+str(dislikeCount180min)+'\n')
    countInfo.write('Comment Count at 3hr:'+str(commentCount180min)+'\n')

    if "viewCount" in sinfo['statistics']:
        countInfo.write('View Count:'+str(viewCount)+'\n')
    else:
        countInfo.write('View Count:NaN'+'\n')

    if "likeCount" in sinfo['statistics']:
        countInfo.write('Like Count:'+str(likeCount)+'\n')
    else:
        countInfo.write('Like Count:NaN'+'\n')

    '''if "dislikeCount" in sinfo['statistics']:
        countInfo.write('Dislike Count:'+str(dislikeCount)+'\n')
    else:
        countInfo.write('Dislike Count:NaN'+'\n')'''

    if "commentCount" in sinfo['statistics']:
        countInfo.write('Comment Count:'+str(commentCount)+'\n')
    else:
        countInfo.write('Comment Count:NaN'+'\n')


#繪圖
chartTitle='Channel: '+Channel+'\n'+'Title: '+Title+'\n'+'Count for 1 day'

#這裡應該能簡化
headers=['time','viewCount','likeCount','commentCount']
dfafter = pd.read_csv('CAS_'+TitleFileName+'.csv', names=headers,header=None,usecols=[0,1,2,3])

t = dfafter['time']

v = dfafter['viewCount']
l = dfafter['likeCount']
#d = dfafter['dislikeCount']
c = dfafter['commentCount']

MaxViewCount=dfafter['viewCount'].max()
MaxLikeCount=dfafter['likeCount'].max()
#MaxDislikeCount=dfafter['dislikeCount'].max()
MaxCommentCount=dfafter['commentCount'].max()
countResult='MaxLikeCount:{0}\nViewCountAt2.5hr:{1}\nViewCountAt3hr:{2}\nMaxViewCount:{3}\nMaxCommentCount:{4}'.format(MaxLikeCount,viewCount150min,viewCount180min,MaxViewCount,MaxCommentCount)
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
#ax3.plot(t,d,'r',label='dislikeCount')
ax3.legend(loc='upper left')
ax3.ticklabel_format(axis='y', style='plain')
ax3.grid(True)

#圖表2
ax4.set_facecolor('lightcyan')
ax4.plot(t,v,'indigo',label='viewCount')
ax4.legend(loc='upper left')
ax4.ticklabel_format(axis='y', style='plain')
ax4.set_ylabel('count')
ax4.grid(True)

#圖表3
ax5.set_facecolor('lightcyan')
ax5.plot(t,c,'darkblue',label='commentCount')
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
fig2.savefig('CCAS_' + TitleFileName + '.png')
print('---儲存完成---')

#結束後輸出
print('Channel:', sinfo['snippet']['channelTitle'])
print('Title:', sinfo['snippet']['title'])
print('Video ID:', sinfo['id'])
if "publishedAt" in sinfo['snippet']:
    print('Stream Created Time(UTC+8):', Stream_Created)
else:
    print('Stream Created Time(UTC+8):NaN')
try:
    if "scheduledStartTime" in sinfo['liveStreamingDetails']:
        print('Planed Start Time(UTC+8):', Planed_Start_Time)
    else:
        print('Planed Start Time(UTC+8):NaN')

    if "actualStartTime" in sinfo['liveStreamingDetails']:
        print('Actual Start Time(UTC+8):', Actual_Start_Time)
    else:
        print('Actual Start Time(UTC+8):NaN')

    if "actualEndTime" in sinfo['liveStreamingDetails']:
        print('Actual End Time(UTC+8):', Actual_End_Time)
    else:
        print('Actual End Time(UTC+8):NaN')
except:
    print('Planed Start Time(UTC+8):NaN')
    print('Actual Start Time(UTC+8):NaN')
    print('Actual End Time(UTC+8):NaN')
print('Log Stop Time(UTC+8): '+str(logStopTime))

if "viewCount" in sinfo['statistics']:
    print('View Count:', sinfo['statistics']['viewCount'])
else:
    print('View Count:NaN')

if "likeCount" in sinfo['statistics']:
    print('Like Count:', sinfo['statistics']['likeCount'])
else:
    print('Like Count:NaN')

'''if "dislikeCount" in sinfo['statistics']:
    print('Dislike Count:', sinfo['statistics']['dislikeCount'])
else:
    print('Dislike Count:NaN')'''

if "commentCount" in sinfo['statistics']:
    print('Comment Count:', sinfo['statistics']['commentCount'])
else:
    print('Comment Count:NaN')
