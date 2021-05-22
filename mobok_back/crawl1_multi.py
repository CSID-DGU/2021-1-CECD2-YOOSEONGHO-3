from selenium import webdriver
import os
import time
from multiprocessing import Pool
from pandas.core.frame import DataFrame
import pandas as pd
import re

elements=['임신·출산','영유아','아동·청소년','청년','중장년','노년','장애인','한부모','다문화(새터민)',
         '저소득층','교육','고용','주거','건강','서민금융','문화']

testE=['아동·청소년']

def crawlWelfares(element):
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

    resultList=[]

    driver.get('http://bokjiro.go.kr/welInfo/retrieveWelInfoBoxList.do')
    print(element,'working...')
    
    tmp=driver.find_element_by_xpath(f"//a[@title='{element}']")
    tmp.click()
    time.sleep(1)
    
    #100개씩 가져오도록 하는 탭 클릭
    driver.find_element_by_css_selector('#pageUnit > option:nth-child(3)').click()
    
    #검색버튼 클릭
    driver.find_element_by_css_selector('#contents > div.catsearchBox > div.inpWrap > div.inpItem.mL10 > fieldset > a').click()
    time.sleep(1)
    
    #현재 페이지 복지 정보
    test=driver.find_element_by_css_selector('#contents > div.resultBox > ul')
    items = test.find_elements_by_tag_name("li")

    #현재 페이지에서 복지정보 추출
    for j in range(len(items)):
        keyNums=items[j].find_element_by_class_name('card_golink')
        
        hrefText=keyNums.get_attribute('href')
        
        refined=re.findall(r'[0-9]+',hrefText)
    
        domain=element
        title=items[j].find_element_by_class_name('tit').text
        desc=items[j].find_element_by_class_name('copy').text
        linko=f'http://bokjiro.go.kr/welInfo/retrieveGvmtWelInfo.do?searchIntClId=01&searchCtgId={int(refined[0])}&welInfSno={int(refined[1])}&pageGb=1&domainName=&firstIndex=0&recordCountPerPage=10&cardListTypeCd=list&welSrvTypeCd=01&searchGb=01&searchWelInfNm=&pageUnit=10&key1=list&stsfCn='
        
        print('유형:',domain)
        print('제목:',title)
        print('내용:',desc)

        data={'유형':domain,'지역':'-','시/군/구':'-','제목':title,'내용':desc,'링크':linko}
        resultList.append(data)

    nextPages=driver.find_element_by_css_selector('#contents > div.resultBox > div')
    pages=nextPages.find_elements_by_tag_name('a')
   
    #다음 페이지 있는지 확인 후 있으면 넘어가서 또 추출
    if pages:
        for pageIndex in range(len(pages)):
            nextPages=driver.find_element_by_css_selector('#contents > div.resultBox > div')
            pages=nextPages.find_elements_by_tag_name('a')
                   
            #다음페이지 클릭
            if pageIndex==0:
                pages[0].click()
                time.sleep(1)
            elif pageIndex<len(pages):
                pages[pageIndex].click()
                time.sleep(1)

            listContainer=driver.find_element_by_xpath('//*[@id="contents"]/div[4]/ul')
            listItems=listContainer.find_elements_by_tag_name('li')

            for j in range(len(listItems)):
                keyNums=listItems[j].find_element_by_class_name('card_golink')
        
                hrefText=keyNums.get_attribute('href')
        
                refined=re.findall(r'[0-9]+',hrefText)

                domain=element
                title=listItems[j].find_element_by_class_name('tit').text
                desc=listItems[j].find_element_by_class_name('copy').text
                linko=f'http://bokjiro.go.kr/welInfo/retrieveGvmtWelInfo.do?searchIntClId=01&searchCtgId={int(refined[0])}&welInfSno={int(refined[1])}&pageGb=1&domainName=&firstIndex=0&recordCountPerPage=10&cardListTypeCd=list&welSrvTypeCd=01&searchGb=01&searchWelInfNm=&pageUnit=10&key1=list&stsfCn='
            
                print('추가페이지 테스트')
                print('유형:',domain)
                print('제목:',title)
                print('내용:',desc)

                data={'유형':domain,'지역':'-','시/군/구':'-','제목':title,'내용':desc,'링크':linko}
                resultList.append(data)
        
    df=DataFrame(resultList,columns=['유형','지역','시/군/구','제목','내용','링크'])
    df.to_csv('./welfare.csv',mode='a', encoding="utf-8-sig")
    driver.quit()
    return
    
if __name__=='__main__':
    pool = Pool(processes=16) 
    pool.map(crawlWelfares, elements) # get_contetn 함수를 넣어줍시다
    
    
    