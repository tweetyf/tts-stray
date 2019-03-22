#!/usr/bin/python
#coding=utf-8
#auther:tweety 2016-01-01
#从百度TTS引擎抓取并生成语音文件
##本文件中 使用多线程模型，提高任务的利用效率。
import os,urllib.request,urllib.parse,urllib.error,urllib.request,urllib.error,urllib.parse,re
import sched,time,socket
import threading 

def getpage(url):
    #print(url)
    req = urllib.request.Request(url)
    req.add_header("User-Agent","Mozilla/5.0 (X11; Ubuntu; Linux x86_64; ) Gecko/20100101 Firefox/21.0")
    u = urllib.request.urlopen(req).read()
    return u

def saveBin(filename, content):
    f = open(filename,mode="ab+")
    f.write(content)
    f.flush()
    f.close()
    
def genTTSUrl(lan,txt,spd):
    ''' 
        generate the BAIDU.COM's TTS url
        lan: language, 'en' for English or 'zh' for Chinese
        txt: the TTS text
        spd: the speedding of read
    '''
    data={
    "lan":lan,
    "pid":101,
    "ie":"UTF-8",
    "spd":spd,
    "text":txt,
    "source":"web"
    }
    #https://fanyi.baidu.com/gettts?lan=zh&text=大家好,。&spd=5&source=web
    ttsUrl = "https://fanyi.baidu.com/gettts?"+urllib.parse.urlencode(data)
    #ttsUrl = "http://tts.baidu.com/text2audio?"+urllib.parse.urlencode(data)
    return ttsUrl

class TaskMaster:
    packs = {}
    results = {}
    thSlaves={} #工作线程
    NSlaves= 20 #工作线程的数量
    spd = 5 #语速
    txtfile="" #文本文件名
    wavfile="" #声音文件名
    lan="" #语言
    packsize =0 #总共有多少个任务
    def __init__(self, txtfile, wavfile, lan):
        print("TaskMgr init()",txtfile, wavfile, lan)
        self.mapPacks(txtfile, wavfile, lan)
        self.packsize = len(self.packs)#记下任务的总数
        
    def mapPacks(self,txtfile, wavfile, lan):
        self.txtfile=txtfile
        self.wavfile=wavfile
        self.lan=lan
        count =0
        f = open(txtfile,mode="r")
        inc1 ="."
        #inc2 =","
        if(lan == "zh"):#中文的简单断句
            inc1 ="。"
            #inc2 ="，"
            self.spd = 5
        if(lan == "en"):#英文的简单断句
            inc1 ="."
            #inc2 =","
            self.spd = 4
        for line in f:
            #简单做一下断句
            sts = line.split(inc1)
            for st in sts:
                if st.isspace(): continue
                count =count+1
                self.packs[count]=st.lower()
        print("finish maped count:",count)
    
    def reducePacks(self):
        while(True):
            print("master thread working... self.results finished:",len(self.results), ' self.packs remains..',len(self.packs))
            time.sleep(5)
            if(len(self.results)< self.packsize):
                continue
            print("all slaves finished working...total:",len(self.results))
            for tid in self.results.keys():
                c = self.results[tid]
                saveBin(self.wavfile,c)
            break
        
    def TTSBaidu(self, tid, txt, lan, spd):
        ''' 
            get the BAIDU.COM's TTS url
            filename: save the txt's Speech in the file with filetype .wav
            lan: language, 'en' for English or 'zh' for Chinese
            txt: the TTS text
            spd: the speedding of read
        '''
        socket.setdefaulttimeout(34.0)
        try:
            #print('processing... ',tid, txt)
            ttsUrl = genTTSUrl(lan ,txt, spd)
            c = getpage(ttsUrl)
            #给master上交结果。
            #print('processing...finished',tid)
            self.results[tid]=c
        except urllib.error.URLError as e:
            print("error:URLError ",e," we will try again...tid:",tid)
            self.TTSBaidu(tid, txt, lan, spd)
        except socket.timeout:
            print("error: TTSBaidu time out!, we will try again...tid:",tid )
            self.TTSBaidu(tid, txt, lan, spd)
        finally:
            pass
                
    def startWork(self):
        #master线程开启
        self.thMaster = threading.Thread(target = self.reducePacks)
        self.thMaster.setDaemon(True)
        self.thMaster.start()
        ## slave线程开始工作
        while (len(self.packs)>0):
            time.sleep(0.05)
            #前一波线程都结束了，开始下一波
            #print('self.packs remains..',len(self.packs))
            if(len(self.thSlaves)==0):
                for slaveID in range(self.NSlaves):
                    if (len(self.packs)==0): break
                    tid ,txt = self.packs.popitem()
                    #print('slave are start working..',tid)
                    t1 = threading.Thread(target = self.TTSBaidu, args=(tid,txt, self.lan, self.spd))
                    self.thSlaves[slaveID]=t1
                    t1.setDaemon(True)
                    t1.start()
            else:
                for slaveID in self.thSlaves.keys():
                    if (len(self.packs)==0): break
                    t1 = self.thSlaves[slaveID]
                    if not t1.is_alive():
                        t1 = self.thSlaves.pop(slaveID)
                        del t1
                        tid ,txt = self.packs.popitem()
                        t1 = threading.Thread(target = self.TTSBaidu, args=(tid,txt, self.lan, self.spd))
                        self.thSlaves[slaveID]=t1
                        t1.setDaemon(True)
                        t1.start()
        self.thMaster.join()

def fileToVoice(txtfile, wavfile, lan):
    '''从文本如何转换为语音文件, 目前支持 中文(zh)和英文(en)
    '''
    a = TaskMaster(txtfile, wavfile, lan)
    a.startWork()
