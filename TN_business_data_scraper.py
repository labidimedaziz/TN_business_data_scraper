from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import time
import re
from time import sleep
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin

filename = "NabeulrRest"
# *********************** 
##go to google maps and search the type of business and the area copy the link and paste it(ex: restaurants in nabeul)
link = "https://www.google.com/maps/search/restaurants+in+Nabeul%E2%80%8E,+Gouvernorat+de+Nabeul/@36.4500749,10.7235444,15z/data=!4m2!2m1!6e5?entry=ttu"
# *********************** 
browser = webdriver.Chrome()
record = []
e = []
le = 0

def Selenium_extractor():

    action = ActionChains(browser)
    a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

    while len(a) < 1000:
        print(len(a))
        var = len(a)
        scroll_origin = ScrollOrigin.from_element(a[len(a)-1])
        action.scroll_from_origin(scroll_origin, 0, 1000).perform()
        time.sleep(2)
        a = browser.find_elements(By.CLASS_NAME, "hfpxzc")

        if len(a) == var:
            le+=1
            if le > 20:
                break
        else:
            le = 0

    for i in range(len(a)):
        scroll_origin = ScrollOrigin.from_element(a[i])
        action.scroll_from_origin(scroll_origin, 0, 100).perform()
        action.move_to_element(a[i]).perform()
        a[i].click()
        time.sleep(2)
        source = browser.page_source
        soup = BeautifulSoup(source, 'html.parser')
        try:
            Name_Html = soup.find('h1', class_= "DUwDvf lfPIob")
            name = Name_Html.text.strip()
            if name not in e:
                e.append(name)
                divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium kR99db"})
                #print(divs)
                Address_Html= divs[0]
                address=Address_Html.text.strip()
                try:
                    for div in divs:
                        if re.search(r'\d{2} \d{3} \d{3}', div.text.strip()):
                            phone = div.text.strip()
                except:
                    pass
                print([name,phone,address])
                record.append((name,phone,address))
    
        except Exception as error: 
            print("An error occurred:", type(error).__name__, error)
            continue
    df=pd.DataFrame(record,columns=['Name','Phone number','Address'])
    df.to_csv(filename + '.csv',index=False,encoding='utf-8')

browser.get(link)
browser.maximize_window()
sleep(7)
Selenium_extractor()

#from selenium import webdriver
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC

#browser.get(link)
#browser.maximize_window()
##WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "DUwDvf lfPIob")))
##Selenium_extractor()
##import requests
##r = requests.get("https://www.google.com/maps/place/Restaurant+pepitos/@36.4354744,10.6178549,13z/data=!4m11!1m3!2m2!1srestaurants+in+Nabeul%E2%80%8E!6e5!3m6!1s0x130298ea4259d12d:0x15ab59dbc331c80a!8m2!3d36.4445258!4d10.7338732!15sChhyZXN0YXVyYW50cyBpbiBOYWJldWzigI5aFyIVcmVzdGF1cmFudHMgaW4gbmFiZXVskgEKcmVzdGF1cmFudOABAA!16s%2Fg%2F11bz9hx_dx?entry=ttu")
#sleep(7)
#soup = BeautifulSoup(browser.page_source, 'html.parser')
#
#Name_Html = soup.find('h1', class_= "DUwDvf lfPIob")
#name = Name_Html.text.strip()
#if name not in e:
#    e.append(name)
#    divs = soup.findAll('div', {"class": "Io6YTe fontBodyMedium kR99db"})
#    print(divs)
#    Address_Html= divs[0]
#    address=Address_Html.text.strip()
#    for div in divs:
#        if re.search(r'\d{2} \d{3} \d{3}', div.text.strip()):
#            phone = div.text.strip()
#    print(name)
#    print(phone) 
#    print(address)
#    browser.quit()
