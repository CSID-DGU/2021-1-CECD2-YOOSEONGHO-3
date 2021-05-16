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
    driver=webdriver.Chrome('./chromedriver')

    driver.implicitly_wait(5)
    driver.get('http://bokjiro.go.kr/welInfo/retrieveLcgWelInfoList.do')

    ##결과 100개씩 가져오도록 하는 부분
    bringNum=driver.find_element_by_css_selector('#pageUnit > option:nth-child(3)').click()

    #지차체만 고르는 부분
    zija=driver.find_element_by_xpath('//*[@id="searchCnDivCd"]/option[2]').click()
    time.sleep(0.5)
    for locationIndex in range(1,18):    
        #서울~제주 드롭박스의 Parent
        locParent=driver.find_element_by_css_selector('#searchSidoCode')
    
        #서울 ~ 제주까지 각 아이템들
        locChild=locParent.find_elements_by_tag_name('option')
    
        #현재 보는 하나의 아이템
        locItem=locChild[locationIndex]
        locText=locItem.text
        #지역 클릭해주고
        locItem.click()
        time.sleep(1)
    
        #시/군/구 Parent 아이템 
        sggLength=len(driver.find_element_by_css_selector('#searchCggCode').find_elements_by_tag_name('option'))
    
        for sggIndex in range(1,sggLength):
            sggParent=driver.find_element_by_css_selector('#searchCggCode')
            sggChilds=sggParent.find_elements_by_tag_name('option')
        
            sggItem=sggChilds[sggIndex]
            sggText=sggItem.text
            #시/군/구 하나 클릭하고
            sggItem.click()
            time.sleep(0.5)
        
            for domainIndex in range(16):
                typeParent=driver.find_element_by_xpath('//*[@title="유형 열기"]')
                typeParent.click()
            
            
                ul=driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/fieldset/div/div/div/ul')
            
                li=ul.find_elements_by_tag_name('li')
            
                theItem=li[domainIndex]

                #db삽입용 복지유형 텍스트
                domain=theItem.text

                #복지유형 하나 클릭하고
                theItem.click()
            
                #검색버튼 클릭
                driver.find_element_by_css_selector('#contents > div.catsearchBox.border.welsearchBox.serviceTypeIn > div.inpWrap > div > fieldset > a').click()
                time.sleep(0.5)
            
            
                #복지정보 추출 
                keyURL='http://bokjiro.go.kr/welInfo/retrieveGvmtWelInfo.do?welInfSno='
                ##가져오기
                listContainer=driver.find_element_by_css_selector('#contents > div.resultBox > ul')
                listItems=listContainer.find_elements_by_tag_name('li')
            
                #결과 없으면 넘김
                if not listItems:
                    #다시 유형 열고
                    typeParent=driver.find_element_by_xpath('//*[@title="유형 열기"]')
                    typeParent.click()
                    #time.sleep(0.5)
            
                    ul=driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/fieldset/div/div/div/ul')
                    li=ul.find_elements_by_tag_name('li')
                    #클릭했던거 해제
                    theItem=li[domainIndex]
                    theItem.click()
                    #time.sleep(0.5)
                    typeParent.click()
                    continue
            
                for liIndex in range(len(listItems)):
                    #db삽입용 복지 제목, 내용, 링크
                    title=listItems[liIndex].find_element_by_tag_name('a').text
                    desc=listItems[liIndex].find_element_by_class_name('copy').text
                    link=listItems[liIndex].find_element_by_tag_name('a').get_attribute('href')
                    link=re.sub(r'[^0-9]', '', link)
                    link=keyURL+link
                
                    #driver2.get(link)
                    #target=driver2.find_element_by_css_selector('#contents > div:nth-child(6) > div.boardViewContent > p:nth-child(1)').text
                
                
                    print('유형:',domain)
                    print('지역:',locText)
                    print('시/군/구:',sggText)
                    print('타이틀: ',title)
                    print('내용:',desc)
                    print('링크:',link)
                    print('\n')
                
                ##다음 페이지 있는지 확인 후 이동
                nextPages=driver.find_element_by_css_selector('#contents > div.resultBox > div')
                pages=nextPages.find_elements_by_tag_name('a')
            
                """페이지가 하나 이상이면 다음 것들 조회하도록 하는 부분인데
                지자체만 검색하면 결과가 매우 적어서 불필요할 듯하다."""
                # if pages:
                #     for pageIndex in range(len(pages)):
                #         nextPages=driver.find_element_by_css_selector('#contents > div.resultBox > div')
                #         pages=nextPages.find_elements_by_tag_name('a')
                   
                #         #다음페이지 클릭
                #         if pageIndex==0:
                #             pages[0].click()
                #         elif pageIndex<len(pages):
                #             pages[pageIndex].click()
                    
                    
                #         listContainer=driver.find_element_by_css_selector('#contents > div.resultBox > ul')
                #         listItems=listContainer.find_elements_by_tag_name('li')
                #         for liIndex in range(len(listItems)):
                #             #db삽입용 복지 제목, 내용, 링크
                #             title=listItems[liIndex].find_element_by_tag_name('a').text
                #             desc=listItems[liIndex].find_element_by_class_name('copy').text
                #             link=listItems[liIndex].find_element_by_tag_name('a').get_attribute('href')
                #             link=re.sub(r'[^0-9]', '', link)
                #             link=keyURL+link
                #             print('유형:',domain)
                #             print('지역:',locText)
                #             print('시/군/구:',sggText)
                #             print('타이틀: ',title)
                #             print('내용:',desc)
                #             print('링크:',link)
                #             print('\n')
                    
                #다시 유형 열고
                typeParent=driver.find_element_by_xpath('//*[@title="유형 열기"]')
                typeParent.click()
                #time.sleep(0.5)
            
                ul=driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/fieldset/div/div/div/ul')
                li=ul.find_elements_by_tag_name('li')
                #클릭했던거 해제
                theItem=li[domainIndex]
                theItem.click()
                #time.sleep(0.5)
                typeParent.click()
    

if __name__=='__main__':
    crawlWelfares()
    