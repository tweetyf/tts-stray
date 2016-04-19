#!/usr/bin/python
#coding=utf-8
#auther:tweety 2016-01-01
#把文本文件们转换成语音
import os,urllib.request,urllib.parse,urllib.error,urllib.request,urllib.error,urllib.parse,re,sys
import tts_baidu
import multiprocessing

def transTest():
     #使用多进程模型，提高CPU利用效率
    numprocs = 8 #有4个核心，4个线程，所以跑4组
    pool = multiprocessing.Pool(processes=numprocs)
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("BBCHeadline.txt","BBCHeadline.wav","en"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("1984.txt","1984.wav","en"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("emma.txt","emma.wav","en"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("Home.2009.eng.txt","Home.2009.eng.wav","en"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("StrayBirds.txt","StrayBirds.wav","en"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("孙子兵法.txt","孙子兵法.wav","zh"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("宇宙尽头的餐馆.txt","宇宙尽头的餐馆.wav","zh"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("爱丽丝镜中奇遇记.txt","爱丽丝镜中奇遇记.wav","zh"))
    pool.apply_async(func =tts_baidu.fileToVoice , args=("狂人日记.txt","狂人日记.wav","zh"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("生命宇宙以及一切.txt","生命宇宙以及一切.wav","zh"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("银河系漫游指南.txt","银河系漫游指南.wav","zh"))
    #pool.apply_async(func =tts_baidu.fileToVoice , args=("鲁宾孙漂流记.txt","鲁宾孙漂流记.wav","zh"))
    pool.close()
    pool.join()
    
def trans_novs():
    # 249 novals gaga
    #使用多进程模型，提高CPU利用效率
    count =0 
    numprocs = 8 #有4个核心，4个线程，所以跑4组
    pool = multiprocessing.Pool(processes=numprocs)
    files = os.listdir("./nov")
    for filename in files:
        if not os.path.isdir(filename):
            if filename.endswith("txt"):
                fname = "./nov/"+filename
                #print fname
                pool.apply_async(func =tts_baidu.fileToVoice , args=(fname,fname+".wav","zh"))
    pool.close()
    pool.join()
    #print "finish all ,total handle TTS GET() :",count

def by_consol():
    if len(sys.argv)<=1:
        print('这样用: \npython tts_file.py 中文文本文件.txt outwavfile.wav zh \n 或者英语版: \npython tts_file.py sometxtfile.txt outwav.wav en')
        exit()
    else:
        txt = sys.argv[1]
        wav = sys.argv[2]
        lan = sys.argv[3]
        tts_baidu.fileToVoice(txt,wav,lan)
       
def main():
    by_consol()
    
if __name__ == '__main__':
    main()
