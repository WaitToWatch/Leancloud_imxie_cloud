# -*- coding: utf-8 -*-

from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

import smtplib
import requests

from bs4 import BeautifulSoup
import time
import sys
import os
from lxml import etree

from flask import Markup

import model

reload(sys)
sys.setdefaultencoding("utf-8")

# 常量
from_addr = 'xcc3641@163.com'
password = '66640013'
# to_addr = ['hugo3641@gmail.com']
smtp_server = 'smtp.163.com'
url = 'http://wufazhuce.com/'


# 编码转换方法
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr))


# 邮件方法
def sendEmail(text, img, title, story):
    mailto = model.query_email()

    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'IMXIE <%s>' % from_addr)
    msg['To'] = _format_addr(','.join(mailto))
    msg['Subject'] = Header(u'The One    ' + title, 'utf-8').encode()
    try:
        msg.attach(to_MIMEText(text=text, img=img, story=story))

        server = smtplib.SMTP(smtp_server, 25)
        server.set_debuglevel(1)

        server.login(from_addr, password)
        server.sendmail(from_addr, mailto, msg.as_string())
        server.close()
    except Exception as e:
        print 'Exception:', e


def test_email(receivers):
    message = MIMEText('遇见你很高兴 (๑′ᴗ‵๑)', 'plain', 'utf-8')
    message['From'] = Header('IMXIE <%s>' % from_addr, 'utf-8')
    message['To'] = Header(receivers, 'utf-8')

    subject = 'ONE 邮件系统测试'
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(smtp_server, 25)  # 25 为 SMTP 端口号
        smtpObj.login(from_addr, password)
        smtpObj.sendmail(from_addr, receivers, message.as_string())
        print "测试邮件发送成功"
        return 'OK'
    except Exception as e:
        print e
        print "测试邮件 Error: 无法发送邮件"
        return 'ERROR'


def http(url):
    html = requests.get(url).text

    page = etree.HTML(html.lower().decode("utf-8"))

    soup_main = BeautifulSoup(html, "lxml")

    # "一个"的文字
    div = soup_main.find_all("div", {"class": "fp-one-cita"})
    text = div[0].a.text
    # print(text)

    # “一个”的图片地址
    img_list = soup_main.find_all("img", {"class": "fp-one-imagen"})
    imgUrl = img_list[0].get('src')
    # print(imgUrl)

    # "一个"的标题
    title_list = soup_main.find_all("p", {"class": "titulo"})
    title = str(title_list[0].text)
    # print(title)

    # 得到文章的地址 用Xpath方法
    url_story = page.xpath("//*[@id=\"main-container\"]/div[1]/div[2]/div/div/div[1]/div/p[2]/a/@href")
    # print(url_story[0])

    soup_stroy = BeautifulSoup(requests.get(url_story[0]).text)
    stroy_content = str(soup_stroy.find("div", {"class": "articulo-contenido"}))

    stroy_title = str(soup_stroy.find("h2", {"class": "articulo-titulo"}))

    stroy = stroy_title + stroy_content

    sendEmail(text, imgUrl, title, stroy)


def get_one_page():
    html = requests.get(url).text

    page = etree.HTML(html.lower().decode("utf-8"))
    # print(page)


    soup_main = BeautifulSoup(html, "lxml")

    # "一个"的文字
    div = soup_main.find_all("div", {"class": "fp-one-cita"})
    text = div[0].a.text
    # print(text)

    # “一个”的图片地址
    img_list = soup_main.find_all("img", {"class": "fp-one-imagen"})
    imgUrl = img_list[0].get('src')
    # print(imgUrl)

    # "一个"的标题
    title_list = soup_main.find_all("p", {"class": "titulo"})
    title = str(title_list[0].text)
    print(title)

    # title = title.replace("VOL.","")
    # # “一个”的文章vol.1132#articulo'
    # url_stroy = 'http://wufazhuce.com/ariticle/' + title
    # # http://wufazhuce.com/article/1326

    # 得到文章的地址 用Xpath方法
    url_story = page.xpath("//*[@id=\"main-container\"]/div[1]/div[2]/div/div/div[1]/div/p[2]/a/@href")
    print(url_story[0])

    soup_stroy = BeautifulSoup(requests.get(url_story[0]).text)
    stroy_content = str(soup_stroy.find("div", {"class": "articulo-contenido"}))

    stroy_title = str(soup_stroy.find("h2", {"class": "articulo-titulo"}))

    stroy = stroy_title + stroy_content

    stroy = Markup(
        '<img class="img-responsive" style="box-shadow:rgb(102, 102, 102) 0.2em 0.2em 0.5em" alt="140x140" src="' + imgUrl + '"></p></div>' +
        '<p style="text-align:center;\"> <br /><br />'
        '<strong><span style="font-size:14px; text-align: center;\">' + text + '</span></strong></p><br /><br /><br /><br /><br />'
        + stroy)
    # print(stroy)
    return stroy


def to_MIMEText(text, img, story):
    return MIMEText('<html><body><div style="text-align: center;">'
                    '<p><img  src="' + img + '"></p></div>' +
                    '<p style="text-align:center;\"> <br /><br />'
                    '<strong><span style="font-size:14px; text-align: center;\">' + text + '</span></strong></p><br /><br /><br /><br /><br />'
                    + story + '</body></html>',
                    'html', 'utf-8')
