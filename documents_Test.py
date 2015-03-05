#!/usr/bin/python
#-*- coding: UTF-8 -*-
'''
Created on 2015年2月14日
@author: Starry
'''
import re,codecs

synatx_after_serialnum = u".,、。，"
format_paragraph_style = []
chinese_num = u"一二三四五六七八九十"


for i in range(10):
    a = []
    format_paragraph_style.append(a)
    a.append(u"第"+chinese_num[i])
    a.append(chinese_num[i])
    a.append(str(i+1))
    
class get_documents(object):
    '''输入路径初始化，处理一个路径下的所有文档，兼容各种文档格式
               处理后可以直接获得的相应的的数据，如token、分句结果、分词结果、
               输出由下列函数实现'''
            
    def __init__(self, filename):
        '''输入处理路径初始化，得到字符串类型的文档集合documents'''
        with codecs.open(filename, "r", "UTF-8") as file1:
            stream = file1.read()
            self.filename = filename[:filename.index(".")]
            #self.paragraphs = cut_paragraph(stream)
            #self.paragraphs = last_filter(last_filter(cut_paragraph(stream)))
            self.paragraphs = self.last_filter(cut_paragraph(stream))
            self.sentences = cut_sentence(self.paragraphs)
            self.summary = []
            
    def last_filter(self, paragraphs):
        """return paragraphs without attachment(except the paper only be a attachment)
             and cut anything after date or lots of dash
        """
        paras = []
        #paragraphs = paragraphs.strip()
        flag = 0
        tag_1 = 0  #用来标记是否匹配到chara里的字符
        tag_2 = 0  #用来标记是否匹配到落款中的日期
        #tag_3 = 0  #用来匹配各种附件的情况
        chara = "'――'".decode('utf8')
        for paragraph in paragraphs:
            #print paragraph
            if (tag_1 == 1) or (tag_2 == 1):
                break 
            #print paragraph
            for char_1 in paragraph:     #1.匹配'――'符号
                if char_1 in chara:
                    print 1 
                    tag_1 = 1
                    break 
            if re.match(u'\d{4}\u5e74\d{1,2}\u6708\d{1,2}\u65e5',paragraph):    #2.简洁版本的正则表达式匹配年月日
            #if re.match(u'\d{4}[\u4e00-\u9fa5]\d{1,2}[\u4e00-\u9fa5]\d{1,2}[\u4e00-\u9fa5]',paragraph):     #此处只匹配了阿拉伯数字的日期如1987年8月7日 未匹配"一九九二年九月八日"模式的中文
                print 2
                tag_2 = 1
            if flag <=5:                      #匹配'附件'
                if re.match(u'\u9644\u4ef6\d+',paragraph):
                    return paragraphs
    
            paras.append(paragraph)
            flag += 1
        return paras
    
    #pass
    
    def first_filter(self, paragraphs):
        """return paragraphs with a meaningfull paragraph as the first paragraph"""
        pass
    
    
    def paragraph_format_detect(self):
        """return yes or no (1 or 0). 
            if the answer is yes modify the self.summary being the summarization 
        """
        global format_paragraph_style
        i = 0
        for paragraph in self.paragraphs:
            if paragraph[0] in format_paragraph_style[i]:
                i += 1
                paragraph = paragraph[1:]
                if paragraph[0] in synatx_after_serialnum:
                    paragraph = paragraph[1:]
                paragraph = paragraph.split(u"。")[0]
                paragraph = paragraph.strip()
                paragraph = str(i).decode("utf-8") + u"." + paragraph
                self.summary.append(paragraph)
        if i >= 2:
            return 1
        else:
            return 0
    
    def get_summary(self, num):
        """return num sentences for the summarization"""
        if self.paragraph_format_detect():
            if len(self.summary) < num:
                num = len(self.summary)
            return ('.').join(self.summary[:num])
    
def cut_paragraph(stream):
    paragraph = []
    stream = stream.strip()
    segments = re.split("\n+",stream)
    #print segments    #打印出unicode编码
    for segment in segments:
        segment = segment.replace("\n","")
        #print segment
        for part in re.split("\s+",segment):
            if part == u"":    
                continue
            #print part
            paragraph.append(part)
    #pa = []
    #for ww in paragraph:
        #ww = ww.replace("\n","")
        #pa.append(ww)  
    return paragraph

def cut_sentence(paragraph):
    sents = []
    posi = []
    left_list = '（(《'.decode('utf8')
    right_list = '）)》'.decode('utf8')
    buf = []
    punt_list = ',!?;~，。！？；～'.decode('utf8')  #string 必须要解码为 unicode 才能进行匹配
    for words in paragraph:
        start = 0
        i = 0  #记录每个字符的位置
        words = words.replace("\n","")
        #words = words.decode('utf8')
        for word in words:
            #don't cut if words in the likes of  ()
            if word in left_list:
                #print word
                buf.append(word)

            if word in right_list and len(buf):
                #print word
                if buf[-1] == left_list[right_list.index(word)]:
                    buf.pop()

            if word in punt_list:
                if len(buf):
                    i += 1
                    continue

                sents.append(words[start:i+1])
                

                #position tags
                if start == 0:
                    posi.append('1')
                else:
                    posi.append('0')
                start = i + 1  #start标记到下一句的开头
                i += 1
            else:
                i += 1  #若不是标点符号，则字符位置继续前移
        if start < len(words):
            sents.append(words[start:])  #这是为了处理文本末尾没有标点符号的情况
            posi.append('-1')
        posi[-1] = '-1'
    return sents, posi


def main():
    document = get_documents("14.txt")
    #text = document.get_summary(5)
    #text = document.paragraphs
    for text in document.paragraphs:
        print text
    
    
if __name__ == "__main__":
    main()