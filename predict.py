# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 10:22:29 2019

@author: Sam
"""

from PIL import Image, ImageFilter
import tensorflow as tf
import numpy as np
import string
import sys
import generate_captcha
import captcha_model

if __name__ == '__main__':
    CKPT_PATH = '/home/sam/tf-captcha/ckpt/capcha_model.ckpt'
    
    captcha = generate_captcha.generateCaptcha()
    width, height, char_num, characters, classes = captcha.get_parameter()

    gray_image = Image.open(sys.argv[1]).convert('L')
    img = np.array(gray_image.getdata())
    test_x = np.reshape(img, [height, width, 1])/255.0
    x = tf.placeholder(tf.float32, [None, height, width, 1])
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width, height, char_num, classes)
    y_conv = model.create_model(x, keep_prob)
    predict = tf.argmax(tf.reshape(y_conv, [-1, char_num, classes]), 2)
    init_op = tf.global_variables_initializer()
    saver = tf.train.Saver()
    gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction = 0.95)
    with tf.Session(config = tf.ConfigProto(log_device_placement = False, gpu_options = gpu_options)) as sess:
        sess.run(init_op)
        saver.restore(sess, CKPT_PATH)
        pre_list =  sess.run(predict, feed_dict={x: [test_x], keep_prob: 1})
        for i in pre_list:
            s = ''
            for j in i:
                s += characters[j]
            print(s)