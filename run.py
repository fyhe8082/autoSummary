#!/usr/bin/python
#coding=utf-8
import os,codecs
import ConfigParser
import threading
from Document import *

threads_num = 1
source_path = './'
destination_path = './'

def main():
    read_configpath()
    #os.system(u"title 自动摘要系统")
    print u"自动摘要系统运行中。。。"
    
    start()
    print u"摘要完成"

def read_configpath():
    global source_path
    global destination_path
    global threads_num
    
    cfg = ConfigParser.ConfigParser()
    try:
        cfg.readfp(open('set.ini'))
    except Exception, e:
        print(e)
        print u'set missing'
    try:
        source_path = cfg.get('summary', 'source_path')
        destination_path = cfg.get('summary', 'destination_path')
        threads_num = cfg.getint('summary', "threads_num")
        
        if not os.path.isdir(source_path):   #判断path是否为路径
            print u"source_path is wrong"
            return
        if not os.path.isdir(destination_path):   #判断path是否为路径
            print u"destination_path is wrong"
            return
        
        print 'source_path', source_path
        print 'destination_path', destination_path
    except Exception, e:
        print(u"读取配置文件出错,请联系QQ:772595904 ")
        print(e)

def start():
    global threads_num
    source_documents_list = []
    for root, dirs, list in os.walk(source_path): 
#root遍历路径，dirs当前遍历路径下的目录，list当前遍历目录下的文件名
        for i in list:
            dir = os.path.join(root, i)    #将分离的部分组成一个路径名
            if dir.split('.')[-1] in ['txt','doc','docx','pdf']:
                source_documents_list.append(dir)
                
    os.chdir(destination_path)
    thread_list = []
    i = 1
    source_documents_list_length = len(source_documents_list)
    if source_documents_list_length < threads_num:
        threads_num = source_documents_list_length
    while (i <= threads_num):
        try:
            t = ThreadClass(source_documents_list[source_documents_list_length * (i-1)/threads_num\
                                                  :source_documents_list_length * i/threads_num])
            print "thread", i, "is running"
            t.start()
            thread_list.append(t)
            i = i + 1
        except Exception, e:
            print e
    for a in thread_list:
        a.join()
  
class ThreadClass(threading.Thread):
    def __init__(self, document_list):
        threading.Thread.__init__(self)
        self.documents_list = document_list

    def run(self):
        for text in self.documents_list:
            document = Document(text)
            summary = document.get_summary(5)
            filename = text.split('\\')[-1]
            filename = filename[:filename.index(".")]
            with codecs.open(filename + ".txt","w","utf-8-sig") as summary_file:
                summary_file.write(summary)
                summary_file.close()


if __name__ == '__main__':
    main()