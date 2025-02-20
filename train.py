# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 10:13:17 2019

@author: User
"""

import tensorflow as tf
import numpy as np
import string
import generate_captcha
import captcha_model
import datetime

if __name__ == '__main__':
    CKPT_PATH = r'D:\Zenii Git\python\tf-captcha\capcha_model.ckpt'
    
    captcha = generate_captcha.generateCaptcha()
    width, height, char_num, characters, classes = captcha.get_parameter()

    x = tf.placeholder(tf.float32, [None, height, width,1])
    y_ = tf.placeholder(tf.float32, [None, char_num * classes])
    keep_prob = tf.placeholder(tf.float32)

    model = captcha_model.captchaModel(width, height, char_num, classes)
    y_conv = model.create_model(x, keep_prob)
    cross_entropy = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(labels=y_, logits=y_conv))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    predict = tf.reshape(y_conv, [-1, char_num, classes])
    real = tf.reshape(y_, [-1, char_num, classes])
    correct_prediction = tf.equal(tf.argmax(predict, 2), tf.argmax(real, 2))
    correct_prediction = tf.cast(correct_prediction, tf.float32)
    accuracy = tf.reduce_mean(correct_prediction)

    saver = tf.train.Saver()
    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        step = 0
        while True:
            batch_x, batch_y = next(captcha.gen_captcha(64))
            _, loss = sess.run([train_step, cross_entropy], feed_dict={x: batch_x, y_: batch_y, keep_prob: 0.75})
            print ('step:%d,loss:%f' % (step,loss))
            
            if step % 100 == 0:
                batch_x_test, batch_y_test = next(captcha.gen_captcha(100))
                acc = sess.run(accuracy, feed_dict={x: batch_x_test, y_: batch_y_test, keep_prob: 1.})
                print ('###############################step:%d,accuracy:%f' % (step,acc), datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
                if acc > 0.99:
                    saver.save(sess, CKPT_PATH)
                    break
            step += 1