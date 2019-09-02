# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 09:40:43 2019

@author: User
"""

from captcha.image import ImageCaptcha, random_color
from PIL import Image
from PIL.ImageDraw import Draw
import numpy as np
import random
import string
from PIL import ImageFilter
import crawl

#def generate_image(self, chars):
#        """Generate the image of the given characters.
#        :param chars: text to be generated.
#        """
#        background = (72, 72, 72)
#        color = (255, 255, 255)
#        im = self.create_captcha_image(chars, color, background)
#        self.create_noise_dots(im, color, number=100)
#        self.create_noise_curve(im, color, lines=1)
#        im = im.filter(ImageFilter.SMOOTH)
#        return im
#    
#@staticmethod
#def create_noise_curve(image, color, lines=1):
#    w, h = image.size
#    
#    for i in range(lines):
#        x1 = random.randint(0, int(w / 5))
#        x2 = random.randint(w - int(w / 5), w)
#        y1 = random.randint(int(h / 5), h - int(h / 5))
#        y2 = random.randint(y1, h - int(h / 5))
#        points = [x1, y1, x2, y2]
#        end = random.randint(160, 200)
#        start = random.randint(0, 20)
#        Draw(image).arc(points, start, end, fill=color)
#    return image
#
#ImageCaptcha.create_noise_curve = create_noise_curve
#ImageCaptcha.generate_image = generate_image

class generateCaptcha():
    def __init__(self,
                 width = 200,#验证码图片的宽
                 height = 60,#验证码图片的高
                 char_num = 5,#验证码字符个数
                 characters = string.digits + string.ascii_uppercase):#验证码组成，数字+大写字母+小写字母  + string.ascii_lowercase
        self.width = width
        self.height = height
        self.char_num = char_num
        self.characters = characters
        self.classes = len(characters)
        self.font = r'C:\Windows\Fonts\arial.ttf'

    def gen_captcha(self, batch_size = 50):
        X = np.zeros([batch_size,self.height,self.width,1])
        img = np.zeros((self.height,self.width), dtype=np.uint8)
        Y = np.zeros([batch_size, self.char_num, self.classes])
        #image = ImageCaptcha(width = self.width, height = self.height, font=self.font, font_sizes=56)
        craw = crawl.Crawl()
        
        while True:
            for i in range(batch_size):
                #captcha_str = ''.join(random.sample(self.characters, self.char_num))
                #img = image.generate_image(captcha_str).convert('L')
                
                craw.Start()
                captcha_str = craw.CaptchaString
                
                img = craw.CaptchaImage
                img = np.array(img.getdata())
                X[i] = np.reshape(img, [self.height, self.width, 1])/255.0
                for j, ch in enumerate(captcha_str):
                    Y[i, j, self.characters.find(ch)] = 1
            Y = np.reshape(Y, (batch_size, self.char_num * self.classes))
            yield X, Y

    def decode_captcha(self,y):
        y = np.reshape(y,(len(y),self.char_num,self.classes))
        return ''.join(self.characters[x] for x in np.argmax(y,axis = 2)[0,:])

    def get_parameter(self):
        return self.width,self.height,self.char_num,self.characters,self.classes

    def gen_test_captcha(self):
        image = ImageCaptcha(width = self.width,height = self.height)
        captcha_str = ''.join(random.sample(self.characters,self.char_num))
        img = image.generate_image(captcha_str)
        img.save(captcha_str + '.jpg')

#gen = generateCaptcha()
#gen.gen_test_captcha()
#gen.gen_captcha(batch_size=1)
