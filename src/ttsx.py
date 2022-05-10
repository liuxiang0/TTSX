""""Use Package: pyttsx3
Solved: rate, volume, voice, save to mp4 or wave format
中英文混排，整篇文件可以采用先读取文本文件内容，再逐一解读。
TODO: 人声选择似乎不能自由选择。支持中文的只有一种。
1、如何分解文本为章节，每章一个应聘文件；这涉及到文本处理问题，识别分章节算法。

"""

import pyttsx3
import os
import time
from sys import argv


def remove(str, special):
    return str.replace(special, "")

def readFile(txt_file):
    '''一次性读取全文'''
    f = open(txt_file,mode='r+t',encoding='utf8')
    return f.read()

def readChapter(txt_file):
    '''按行读取，判断章节，分章节输出list'''
    keepRes = []
    with open(txt_file, mode='r+t',encoding='utf8') as fHandler:
        txtLines = fHandler.readlines()
        for line in txtLines:
            #line = line.strip()
            if line != '\n': # skip blank line 空白行跳过
                if '#' in line:
                    line = remove(line,"#")
                keepRes.append(line)
    
    return " ".join(keepRes)
     

def onStart(name):
    print('开始', name)

def onWord(name, location, length):
    print('说者', name, location, length)
    if location > 10:  # interrupt an utterance
        Lille.stop()

def onEnd(name, completed):
    print('结束', name, completed)


if __name__ == '__main__':
    if len(argv) < 2:
        print("""将指定目录下指定后缀的所有文本文件批量进行语音转换。
        使用说明: python ttsx.py 输入目录名 文件名后缀 输出目录名
        使用举例: python ttsx.py input_dir md output_dir
        """)
        exit()

    start = time.time()
        
    DIRNAME = argv[1] if len(argv) > 1 else "input"
    extends = argv[2] if len(argv) > 2 else "md"
    fileList = [name for name in os.listdir(DIRNAME) \
        if name.endswith(extends)]  #指定文本文件
    save_dir = argv[3] if len(argv) > 3 else DIRNAME+'Vow'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    Lille = pyttsx3.init()  # object creation
    #Lille.connect('started-utterance', onStart)
    Lille.connect('started-word', onWord)
    #Lille.connect('finished-utterance', onEnd)
    '''
    voices = Lille.getProperty('voices')
    for voice in voices:
        Lille.setProperty('voice', voice.id) # change voices
        Lille.say('The quick brown fox jumped over the lazy dog.')
    '''
    rate = Lille.getProperty('rate')
    Lille.setProperty('rate', rate-30) #change rate 200是正常速度，300较快，[0,500]
    #rate = Lille.getProperty('rate')
    '''
    voices = Lille.getProperty('voices') # 查看语音引擎
    #说者 声音HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ZH-CN_HUIHUI_11.0 1 124972
    # Lille.setProperty('voice', voices[0].id) # 0支持中英文

    volume = Lille.getProperty('volume')
    Lille.setProperty('volume', volume-0.3) # [0,1] default 1
    #volume = Lille.getProperty('volume')

    Lille.say('使用的语速为' + str(rate),'语速'+str(rate)) #200 没有改变
    Lille.say('使用的音量为' + str(volume),'音量'+str(volume)) #1.0 似乎没有改变
    #Lille.say('使用的声音为' + str(voices[0].id),'声音'+str(voices[0].id))

    Lille.runAndWait()
    '''

    for file in fileList:
        fn = os.path.join(DIRNAME, file)
        #txtCN = readFile(fn)
        txtCN = readChapter(fn) # readlines()
        #print(txtCN)
        '''
        Lille.say(txtCN,'文章')
        Lille.runAndWait()
        Lille.stop()'''
        """Saving Voice to a file"""
        # On linux make sure that 'espeak' and 'ffmpeg' are installed, 
        # support wave mp3 ...
            
        save_file = os.path.join(save_dir, file.split('.')[0]+".mp3")
        Lille.save_to_file(txtCN, filename=save_file)

    Lille.runAndWait()
    Lille.stop()
    print("运行{0}，耗时{1}秒！".format(DIRNAME, time.time()-start))
