#!/usr/bin/python
#coding=utf-8
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
        with codecs.open(filename, "r", "utf-8") as file:
            stream = file.read()
            self.filename = filename[:filename.index(".")]
            self.paragraphs = cut_paragraph(stream)
            #self.paragraphs = last_filter(first_filter(cut_paragraph(stream)))
            self.sentences = cut_sentence(self.paragraphs)
            self.summary = []
            
    def last_filter(self, paragraphs):
        """return paragraphs without attachment(except the paper only be a attachment)
             and cut anything after date or lots of dash"""
        pass
    
    def first_filter(self, paragraphs):
        """return paragraphs with a meaningfull paragraph as the first paragraph"""
        pass
    
    
    def paragraph_format_detect(self):
        """return yes or no (1 or 0). 
            if the answer is yes modify the self.summary being the summarization """
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
    segments = re.split("\n\n+",stream)
    for segment in segments:
        segment = segment.replace("\n","")
        for part in re.split("\s\s+",segment):
            if part == u"":
                continue
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
    document = get_documents("14.txt")
    text = document.get_summary(5)
    print text
    
if __name__ == "__main__":
    main()