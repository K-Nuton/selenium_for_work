import time

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import element_to_be_clickable as CLICKABLE
from executor import Executor

executor = Executor.open('http://www.htmq.com/html/select.shtml')

executor.find('//*[@id="content_left"]/div[7]/form/p[2]/select').by(By.XPATH).And().select(1)\
        .find('//*[@id="cse-search-box"]/div/input[4]').by(By.XPATH).And().send('うんこが美味しい')\
        .find('//*[@id="cse-search-box"]/div/input[5]').by(By.XPATH).until(CLICKABLE).And().click()

time.sleep(3600)
