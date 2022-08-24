from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
import pymysql
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os, time, traceback
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_login(userId,password):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(executable_path="/var/www/html/master/chromedriver",chrome_options=chrome_options)

    try:
        driver.get('https://cyber.anyang.ac.kr/Main.do?cmd=viewHome')
        pop = driver.find_element(By.XPATH,'/html/body/div[4]/div[1]/button')
        pop.click()

        ul = driver.find_element(By.CLASS_NAME, 'user_box')
        Id = ul.find_element(By.ID,'id')
        pwd = ul.find_element(By.ID,'pw')

        Id.send_keys(userId)
        pwd.send_keys(password)
        pwd.send_keys(Keys.RETURN)
        try:
            WebDriverWait(driver,3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            return 0
        except:
            return 1
    except Exception as e:
        traceback.print_exc()
        return 0
    finally:
        driver.close()
        driver.quit()