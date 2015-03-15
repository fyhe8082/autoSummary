#!/usr/bin/python
#coding=utf-8
import re,codecs
from django.contrib.webdesign.lorem_ipsum import paragraph
from cgi import log
from documents_Test import chinese_num


format_paragraph_serialnum = []
synatx_after_serialnum = u".,、。，"

def init_format_paragraph_serialnum():
    chinese_num = u"一二三四五六七八九十"
    
    for i in range(10):
        a = []
        format_paragraph_serialnum.append(a)
        a.append(u"第"+chinese_num[i])
        a.append(chinese_num[i])
        a.append(str(i+1))
        a.append(u"（"+chinese_num[i])

init_format_paragraph_serialnum()

class Document(object):
            
    def __init__(self, filename):
        with codecs.open(filename, "r", "utf-8") as file:
            stream = file.read()
            self.filename = filename[:filename.index(".")]
            self.paragraphs = self.del_footpart(cut_paragraph(stream))
            self.sentences = cut_sentence(self.paragraphs)
            self.summary = []

    def get_summary(self, num):
        """return num sentences for the summarization"""
        if self.get_formatpart():
            if len(self.summary) < num:
                num = len(self.summary)
            return ('\n').join(self.summary[:num])
            
    def del_footpart(self, paragraphs):
        """return paragraphs without attachment(except the paper only be a attachment)
             and cut anything after date or lots of dash"""
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
                #print 2
                tag_2 = 1
            if flag <=5:                      #匹配'附件'
                if re.match(u'\u9644\u4ef6\d+',paragraph):
                    return paragraphs
    
            paras.append(paragraph)
            flag += 1
        return paras
    
    def del_headpart(self, paragraphs):
        """return paragraphs with a meaningful paragraph as the first paragraph"""
        pass
    
    
    def get_formatpart(self):
        """return yes or no (1 or 0). 
            if the answer is yes modify the self.summary being the summarization """
        global format_paragraph_serialnum
        serialNum = 0
        flag = []
        serialNumSecond = 9
         
        for i ,paragraph in enumerate(self.paragraphs):
            if (paragraph[0] in format_paragraph_serialnum[0]) or \
                            paragraph[:2] in format_paragraph_serialnum[0]:
                
                if (paragraph[0] in format_paragraph_serialnum[0]):
                    flag.append(format_paragraph_serialnum[0].index(paragraph[0]))
                elif paragraph[:2] in format_paragraph_serialnum[0]:
                    flag.append(format_paragraph_serialnum[0].index(paragraph[:2]))
                
                if len(flag) == 1:
                    self.mainpart = self.paragraphs[:i]
                elif len(flag) == 2:
                    serialNumSecond = 0
                    
            if  len(flag) >= 2 and (paragraph[0] == format_paragraph_serialnum[serialNumSecond][flag[1]]  or \
                            paragraph[:2] == format_paragraph_serialnum[serialNumSecond][flag[1]]):
                serialNumSecond += 1
                paragraph = paragraph.split(u"。")[0]
                paragraph = paragraph.strip()
                self.summary.append("    "+paragraph)
                continue
            
            if len(flag) >= 1 and (paragraph[0] == format_paragraph_serialnum[serialNum][flag[0]] or \
                            paragraph[:2] == format_paragraph_serialnum[serialNum][flag[0]]):
                serialNum += 1
                serialNumSecond = 9
                while(len(flag) > 1):
                    flag.pop()
                paragraph = paragraph.split(u"。")[0]
                paragraph = paragraph.strip()
                self.summary.append(paragraph)
                continue
                
        if serialNum >= 2:
            return 1
        else:
            return 0
    
    
def cut_paragraph(stream):
    paragraph = []
    stream = stream.strip()
    segments = re.split("\n\n+",stream)
    for segment in segments:
        segment = segment.replace("\n","")
        for part in re.split("\s\s+",segment):
            if part == u"":
                continue
            paragraph.append(part) 
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
                buf.append(word)

            if word in right_list and len(buf):
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
    document = Document("14.txt")
    text = document.get_summary(20)
    print text
    
if __name__ == "__main__":
    main()