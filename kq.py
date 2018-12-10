from selenium import webdriver
from PIL import Image
import pytesseract
import time
import os
import getpass
import datetime
import sys


user = ''
pwd = ''
arrive_time = ''
leave_time = ''


# 用户输入打卡时间
def get_time():

    global arrive_time
    global leave_time

    arrive_time = input('请输入上班时间(例: 08:30): ')
    leave_time = input('请输入下班时间(例: 17:30): ')


# 用户输入user和pass
def get_user_and_pass():

    global user
    global pwd

    user = input('请输入用户名: ')
    pwd = getpass.getpass('请输入密码: ')


# 二值化验证码图像
def binaryzation(image, threshold):
    image = image.convert('L')
    table = []
    for i in range(256):
        if i > threshold:
            table.append(0)
        else:
            table.append(1)

    return image.point(table, '1')


# 打卡
def do_kq(check_pass = False):
    driver = webdriver.Chrome()
    driver.get('http://kq.neusoft.com/')

    textfields = driver.find_elements_by_class_name('textfield')

    # print(len(textfields))

    user_field = textfields[0]
    pass_field = textfields[1]

    user_field.send_keys(user)
    pass_field.send_keys(pwd)

    time.sleep(5)

    driver.save_screenshot('login.png')

    image = Image.open('login.png')

    # 这个裁剪的尺寸会根据显示器变化，可以用画图编辑
    t = (568, 347, 630, 373)

    frame = image.crop(t)

    frame.save('code.png')

    image = Image.open('code.png')

    image = binaryzation(image, threshold=127)

    code = pytesseract.image_to_string(image)

    print('the code is', code)

    code_field = driver.find_element_by_class_name('a')
    code_field.send_keys(code)

    os.remove('login.png')
    os.remove('code.png')

    time.sleep(5)

    driver.find_element_by_id('loginButton').click()

    time.sleep(5)

    if check_pass is True:
        try:
            driver.find_element_by_class_name('mr36')
            print('设置成功！程序将在 ', arrive_time, ' 和 ', leave_time, ' 打卡。')
        except:
            print('密码错误')
            sys.exit()

    else:
        driver.find_element_by_class_name('mr36').click()

        time.sleep(5)

        now = datetime.datetime.now()
        print(str(now)[0:19], ' 成功打卡了！')

    driver.close()
    driver.quit()

def check_time():

    now = datetime.datetime.now()
    hour_and_minute = str(now)[11:16]

    if hour_and_minute == arrive_time or hour_and_minute == leave_time:
        return True

    return False


# 模拟打卡
def do_fake_kq():
    print('模拟打卡了！')


def main():
    get_user_and_pass()
    get_time()

    do_kq(check_pass=True)

    while True:
        time.sleep(1)

        if check_time():
            do_kq()
            time.sleep(60)


if __name__ == '__main__':
    main()