#name:超星继续教育自动化学习软件
#author:林立
#date:2023.12.15

#environment
'''python3.9'''
'''基于selenium4.15'''
'''基于chromedriver'''

# bug
'''未加入异常处理语句'''
'''未加入验证码处理功能'''


from selenium import webdriver
from time import sleep
from datetime import datetime
# from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

option = webdriver.ChromeOptions()
'''本句能让浏览器不出现机器控制字样'''
option.add_experimental_option('excludeSwitches', ['enable-automation'])
'''本句能让浏览器保持显示不关闭'''
option.add_experimental_option('detach', True)
browser = webdriver.Chrome(options=option)
'''需要的话可以调整窗体大小'''
# browser.set_window_size(600,400)
browser.get('https://mjxy.px.chaoxing.com/portal/login')
browser.implicitly_wait(10)#显式等待
browser.find_element('id', 'userName').send_keys('18950476918')#输入用户名
browser.find_element('id', 'passWord').send_keys('edu@476918')#输入密码
'''10秒等待人工输入验证码并登录'''
sleep(10)
'''穿插断言，利用print打印出程序运行的阶段性结果'''
print(browser.current_url)
'''以下开始自动化挂机学习'''
'''通过完全路径定位到’个人课程‘元素，并打开相关页面'''
browser.find_element('xpath', '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/a[2]').click()
'''切换框架，这里要特别注意WebDriver只能定位一个页面上元素，处到不同框架页面时要通过切换才能定位到'''
browser.switch_to.frame('frame_content')
sleep(1)
Class = browser.find_elements(By.LINK_TEXT, '进入学习')
print('您总共有%d个主题课程要学习'%len(Class))#课程总数量
'''开始循环主题课程'''
for ClassNO in range(len(Class)):
    browser.find_elements(By.LINK_TEXT, '进入学习')[ClassNO].click()  # 进入课程
    sleep(1)
    '''这里由于浏览器打开了新的窗体，要通过窗体句柄实现切到新打开的窗体'''
    handles = browser.window_handles
    browser.switch_to.window(handles[-1])
    '''进入当前主题课程下的具体课表'''
    browser.switch_to.frame('frame_content-zj')
    sleep(1)
    lesson = browser.find_elements(By.TAG_NAME, 'li')
    print('现在学习的主题课程共有%d节课'%len(lesson))
    lesson[0].click()
    browser.find_element(By.ID, 'iframe').click()
    sleep(1)
    '''开始循环当前主题课程下的课时'''
    for lessonNO in range(len(lesson)):
        lessonbr = browser.find_elements(By.XPATH, '//*[@id="coursetree"]/ul/li/div[2]/ul/li')[lessonNO]
        sleep(1)
        lessonbr.click()
        sleep(2)
        textContent = lessonbr.find_element(By.CLASS_NAME, 'prevHoverTips').get_attribute('textContent')
        print(textContent)
        sleep(1)
        if textContent != '已完成':
            browser.find_element(By.ID, 'iframe').click()
            browser.switch_to.frame('iframe')
            sleep(1)
            videoframe = browser.find_element(By.CSS_SELECTOR, '#ext-gen1050 > iframe')
            '''  browser.find_element(By.XPATH,'//*[@id="ext-gen1050"]/iframe')   '''
            sleep(1)
            browser.switch_to.frame(videoframe)
            videospeed = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]')
            videospeedbutton = browser.find_element(By.XPATH,'//*[@id="video"]/div[5]/div[1]/button')
            curtime = browser.find_element(By.XPATH, '//*[@id="video"]/div[5]/div[2]/span[2]')
            videotime = browser.find_element(By.XPATH, '//*[@id="video"]/div[5]/div[4]/span[2]')
            sleep(1)
            # browser.execute_script("arguments[0].innerText = '2x';", videospeed)
            print(videospeed.text)
            '''这里将视频观看速度调为2倍速，按一次button速度改变0.25'''
            while videospeed.text != '2x':
                videospeedbutton.click()
                sleep(1)
                videospeed = browser.find_element(By.XPATH,
                                                  '/html/body/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]')
            print('开始学习第'+str(ClassNO+1)+'个主题，第'+str(lessonNO+1)+'节课')
            print('当前视频已看'+curtime.text)
            timestr1 = curtime.text
            if len(timestr1)<6:
                timestr1 = '0:'+timestr1
            print('当前视频总时长'+videotime.text)
            timestr2 = videotime.text
            if len(timestr2)<6:
                timestr2 = '0:'+timestr2
            time1 = datetime.strptime(timestr1, '%H:%M:%S')
            time2 = datetime.strptime(timestr2, '%H:%M:%S')
            passtime=(time2 - time1).seconds
            print('需要再看'+str(passtime//2)+"秒")
            '''每节课学习时长，这里注意时间的换算，按2倍速时间减半'''
            sleep(passtime//2)  # 每节课学习时长，剩余时长一半取整
            sleep(2)
            '''注意跳回到最外层页面'''
            browser.switch_to.default_content()
    '''关闭当前窗口，避免被系统检测到双开'''
    browser.execute_script("window.close();")#关闭当前窗口
    '''跳回最早打开的窗体'''
    browser.switch_to.window(handles[0])
    sleep(1)
    browser.switch_to.frame('frame_content')

##########################################################################
# 1:20:19

# 超星继续教育分主题半自动化

# from selenium import webdriver
# from time import sleep
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.by import By
# option = webdriver.ChromeOptions()
# option.add_experimental_option('excludeSwitches', ['enable-automation'])
# option.add_experimental_option('detach', True)
# browser = webdriver.Chrome(options=option)
# browser.get('https://mjxy.px.chaoxing.com/portal/login')
# browser.implicitly_wait(10)
# browser.find_element('id', 'userName').send_keys('18950476918')
# browser.find_element('id', 'passWord').send_keys('edu@476918')
# sleep(10)
# print(browser.current_url)
# browser.find_element('xpath', '/html/body/div[2]/div[1]/div[2]/div/div[1]/div/a[2]').click()
# Classurl = browser.current_url
# browser.switch_to.frame('frame_content')
# sleep(1)
# Class = browser.find_elements(By.LINK_TEXT, '进入学习')
# print(len(Class))  # 课程总数量
# '''选课程'''
# browser.find_elements(By.LINK_TEXT, '进入学习')[6].click()  # 进入课程
# sleep(1)
# handles = browser.window_handles
# browser.switch_to.window(handles[-1])
# '''进入课表'''
# browser.switch_to.frame('frame_content-zj')
# sleep(1)
# lesson = browser.find_elements(By.TAG_NAME, 'li')
# print(len(lesson))
# lesson[0].click()
# browser.find_element(By.ID, 'iframe').click()
# sleep(1)
# for lessonNO in range(len(lesson)):
#     lessonbr = browser.find_elements(By.XPATH, '//*[@id="coursetree"]/ul/li/div[2]/ul/li')[lessonNO]
#     sleep(1)
#     lessonbr.click()
#     sleep(2)
#     textContent = lessonbr.find_element(By.CLASS_NAME, 'prevHoverTips').get_attribute('textContent')
#     print(textContent)
#     sleep(1)
#     if textContent == '已完成':
#         sleep(1)
#         browser.find_element(By.ID, 'iframe').click()
#         browser.switch_to.frame('iframe')
#         sleep(1)
#         vframe = browser.find_element(By.CSS_SELECTOR, '#ext-gen1050 > iframe')
#         '''  browser.find_element(By.XPATH,'//*[@id="ext-gen1050"]/iframe')   '''
#         sleep(1)
#         browser.switch_to.frame(vframe)
#         speed = browser.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[1]/div[5]/div[1]/div[2]')
#         curtime = browser.find_element(By.XPATH, '//*[@id="video"]/div[5]/div[2]/span[2]')
#         videotime = browser.find_element(By.XPATH, '//*[@id="video"]/div[5]/div[4]/span[2]')
#         sleep(1)
#         browser.execute_script("arguments[0].innerText = '2.0x';", speed)
#         print(speed.text)
#         print(curtime.text[:-3])
#         print(videotime.text[:-3])
#         sleep(10)  # 每节课学习时长







