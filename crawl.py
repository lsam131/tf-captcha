# -*- coding: utf-8 -*-
"""
Created on Tue Jul 23 15:55:54 2019

@author: Sam
"""

from bs4 import BeautifulSoup
import requests
import base64
from PIL import Image



URL = 'http://192.168.1.163/Captcha/Default.aspx'
CAPTCHA_TEMP = 'tempCaptcha.jpg'
INTERVAL = 5

class Crawl():
    def __init__(self):
        self.Sess = requests.Session()
        self.CaptchaString = ''
        self.CaptchaImage = None
        
    def Start(self):
        respone = self.Sess.get(URL, stream=True)
        if respone.status_code == 200:
            soup = BeautifulSoup(respone.content, "html.parser")
            imgtag = soup.find(id='Image1').get('src')
            img_string = imgtag.split(',')[-1]
            bin_img_data = base64.b64decode(img_string)
            with open(CAPTCHA_TEMP, 'wb') as f:
                f.write(bin_img_data)
            self.CaptchaImage = Image.open(CAPTCHA_TEMP).convert('L')
            self.CaptchaString = soup.select_one('#CaptchaCode').text
            

#crawl = Crawl()
#crawl.Start()
#crawl.CaptchaImage.show()
#print(crawl.CaptchaString)