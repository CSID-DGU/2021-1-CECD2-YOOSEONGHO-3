from selenium import webdriver
from bs4 import BeautifulSoup
import os
import django
import time
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "jangoback.settings")

django.setup()
from welfare.models import Welfare

def crawlWelfares():
    #배포용
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument("--disable-dev-shm-usage")
    # chrome_options.add_argument("--no-sandbox")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

    #일반용
    option= webdriver.ChromeOptions()
    option.add_argument('headless')
    driver=webdriver.Chrome('./chromedriver',options=option)

    driver.implicitly_wait(5)

    elements=['임신·출산','영유아','아동·청소년','청년','중장년','노년','장애인','한부모','다문화(새터민)',
         '저소득층','교육','고용','주거','건강','서민금융','문화']

    tmp=''

    for i in range(len(elements)):
        driver.get('http://bokjiro.go.kr/welInfo/retrieveWelInfoBoxList.do')
        print('working...')
    
        tmp=driver.find_element_by_xpath(f"//a[@title='{elements[i]}']")
        tmp.click()
    
        tmp2=driver.find_element_by_css_selector('#pageUnit > option:nth-child(3)').click()
    
        tmp3=driver.find_element_by_css_selector('#contents > div.catsearchBox > div.inpWrap > div.inpItem.mL10 > fieldset > a')
        tmp3.click()      
    
        test=driver.find_element_by_css_selector('#contents > div.resultBox > ul')
        items = test.find_elements_by_tag_name("li")
    
        for j in range(len(items)):
            keyNums=items[j].find_element_by_class_name('card_golink')
        
            hrefText=keyNums.get_attribute('href')
        
            refined=re.findall(r'[0-9]+',hrefText)
    
            do=elements[i]
            t=items[j].find_element_by_class_name('tit').text
            d=items[j].find_element_by_class_name('copy').text
            linko=f'http://bokjiro.go.kr/welInfo/retrieveGvmtWelInfo.do?searchIntClId=01&searchCtgId={int(refined[0])}&welInfSno={int(refined[1])}&pageGb=1&domainName=&firstIndex=0&recordCountPerPage=10&cardListTypeCd=list&welSrvTypeCd=01&searchGb=01&searchWelInfNm=&pageUnit=10&key1=list&stsfCn='
            
            welfare=Welfare.objects.filter(domain=do,title=t)
            if not welfare:
                Welfare(domain=do,title=t,description=d,link=linko).save()
        
    
if __name__=='__main__':
    crawlWelfares()
    