# coding:utf8
__author__ = 'MisT'

import requests
import json
import re
import time
from urllib import urlencode
from config import *


meta_url = "https://bh3773.class.gaoxiaobang.com/class/"+chapter+"/quiz"
meta_headers={"Cookie":cookie,"User-Agent":user_agent}

print "当前课程编号："+chapter
print "正在获取章节测试列表..."
r=requests.get(meta_url,headers=meta_headers)
# print r.status_code
# print r.text
t=r.text.encode('gbk')
content_ids=re.findall('contentId\":\"(.*?)\"',t)
print "\r章节测试列表获取完毕：",content_ids
for id in content_ids:
    id=str(id)
    url = meta_url+"/"+id
    print "======================"
    print "测试编号："+id
    print "URL：",url
    r=requests.get(url,headers=meta_headers)

    # print r.status_code
    t=r.text.encode('gbk')
    # print t

    print "已打开URL，正在获取题目及答案..."
    t=r.text.encode('utf-8',errors='ignore')
    items=re.findall('questionList.*];',t)
    submit=re.findall('quizSubmit\(.*\);',t)
    # print submit
    submit=re.findall('[0-9]{13}',submit[0])
    # print submit
    data=items[0].replace('\'','\"')
    data=re.findall('\[.*]',data)
    ql=json.loads(data[0])
    # print ql
    quizSubmission = []
    for x in ql:
        # print x['name']
        question={"question_id":x['questionId'].encode('utf-8'),'text':[]}
        ans=x['answerList']
        for a in ans:
            correct=False
            if a['correct']=='1':
                correct=True
                question['text'].append(a['answerId'].encode('utf-8'))
            # print a['text'],correct
        quizSubmission.append(question)

    print "已获取题目及答案，共%d道题目，正在提交..." % (len(quizSubmission))
    submission_url="https://bh3773.class.gaoxiaobang.com/class/"+chapter+"/quiz/"+id+"/submission/api"
    form=\
        {
            # 'startTime':str(int(round(time.time() * 1000))),
            'startTime':submit[0],
            'quizSubmission':quizSubmission
        }
    # print form
    headers = \
        {
            'Host': 'bh3773.class.gaoxiaobang.com',
            'User-Agent': user_agent,
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Accept-Encoding': 'gzip, deflate, br',
            # 'Referer': 'https://bh3773.class.gaoxiaobang.com/class/19539/quiz/111041',
            'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Content-Length': '428',
            'Cookie': cookie,
            'Connection': 'keep-alive'
        }
    params=str(int(round(time.time() * 1000)))
    data = urlencode(form)
    # print data
    r=requests.post(submission_url,params=params,data=data,headers=headers)
    # print r.url
    # print r.status_code
    # print r.text
    print "完成。"



