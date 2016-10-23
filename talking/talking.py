# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import urllib
import urllib2
import json
import uuid
import base64
import os
import time
#from renti import *

#获取百度token
appid=8757898
apikey="UstfHllbqAZ9jKKTAOOfDurY"
secretkey="2d4ab26f5d485f8c9fcbb396ddddb16d"

baidu_url="https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apikey + "&client_secret=" + secretkey;

y_post=urllib2.urlopen(baidu_url)
y_read=y_post.read()
y_token=json.loads(y_read)['access_token']
#print y_read
#print y_token

#------------------function-------------

def luyin():
        os.system('arecord -D plughw:1,0 -c 1 -d 5 1.wav -r 8000 -f S16_LE 2>/dev/null')

def fanyi():
        #http://vop.baidu.com/server_api?lan=zh&cuid=***&token=***
        #---------------语音识别部分

        mac_address="raspberrypi3"
        with open("1.wav",'rb') as f:
            s_file = f.read()


        speech_base64=base64.b64encode(s_file).decode('utf-8')
        speech_length=len(s_file)

        data_dict = {'format':'wav', 'rate':8000, 'channel':1, 'cuid':mac_address, 'token':y_token, 'lan':'zh', 'speech':speech_base64, 'len':speech_length}
        json_data = json.dumps(data_dict).encode('utf-8')
        json_length = len(json_data)

        asr_server = 'http://vop.baidu.com/server_api'

        request = urllib2.Request(url=asr_server)
        request.add_header("Content-Type", "application/json")
        request.add_header("Content-Length", json_length)
        fs = urllib2.urlopen(url=request, data=json_data)
        result_str = fs.read().decode('utf-8')
        json_resp = json.loads(result_str)
        if json_resp.has_key('result'):
                out_txt=json_resp['result'][0]
        else:
                out_txt="Null"
        return out_txt

def tuling(b):
        tulingKey = '1107d5601866433dba9599fac1bc0083'
        f=urllib.urlopen("http://www.tuling123.com/openapi/api?key=" + tulingKey + "&info=%s" % b)
        f=json.loads(f.read())['text']
        return f

def hecheng(text,y_token):
        #text="你好我是机器人牛牛很高兴能够认识你"
        geturl="http://tsn.baidu.com/text2audio?tex="+text+"&lan=zh&per=1&pit=9&spd=6&cuid=CCyo6UGf16ggKZGwGpQYL9Gx&ctp=1&tok="+y_token
        return os.system('omxplayer "%s" > /dev/null 2>&1 '%(geturl))
        #return os.system('omxplayer "%s" > /dev/null 2>&1 '%(geturl))

def nowtime():
        return time.strftime('%Y-%m-%d %H:%M:%S ')


#---------------main-----------------
num=0   #num用来判断是第一次说话，还是在对话过程中
first=1 #判断是不是第一说话  当1000次没有人动认为是第一次
while True:
        #if ganying()!=0:
                run=open('run.log','a')
                if first==0:
                        hecheng("你好,我是牛牛机器人,你可以和我聊天,不过说话的时候你必须靠近话筒近一点,",y_token)
                        hecheng("说点什么吧,2秒钟内说完哦.",y_token)
                        first=1                 #为1一段时间就不执行
                        num=0                   #从新计数

                #print ganying()
                run.write(nowtime()+"说点神马吧..........."+'\n')
                print nowtime()+"说点神马吧.........."
                luyin()                         #开始录音
                out=fanyi().encode("utf-8")     #翻译文字
                run.write(nowtime()+"我说:"+out+'\n')
                print nowtime()+"我说:"+out
                if out == "Null":
                        text="没有听清楚你说什么"
                        os.system('omxplayer "shenme.wav" > /dev/null 2>&1 ')

                else:
                        text=tuling(out)
                        hecheng(text,y_token)
                print nowtime()+"牛牛:"+text
                run.write(nowtime()+"牛牛:"+text+'\n')
                run.close()
        #else:
                #print ganying()        #调试查看是否为0有人没人
                #print num
        #        num=num+1               #num长时间增大说明没有人在旁边
        #        if num > 1000:
        #                first=0         #0表示第一次说话