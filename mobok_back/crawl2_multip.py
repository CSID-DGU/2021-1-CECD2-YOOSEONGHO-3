# -*- coding: utf-8 -*-
from pandas.core.frame import DataFrame
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import re
from multiprocessing import Pool
import pandas as pd

areaSelectors=[]
for i in range(2,19):
    selector=f'#searchSidoCode > option:nth-child({i})'
    areaSelectors.append(selector)
    
    
def crawlByArea(area):
    print('크롤링 시작')

    resultList=[]
    
    #각 처리마다 드라이버 하나 필요
    option= webdriver.ChromeOptions()
    option.add_argument('headless')
    driver=webdriver.Chrome('./chromedriver')
    driver2=webdriver.Chrome('./chromedriver')

    driver.implicitly_wait(3)
    driver.get('http://bokjiro.go.kr/welInfo/retrieveLcgWelInfoList.do')
    
    ##결과 100개씩 가져오도록 하는 부분
    driver.find_element_by_css_selector('#pageUnit > option:nth-child(3)').click()

    #지차체만 고르는 부분
    driver.find_element_by_xpath('//*[@id="searchCnDivCd"]/option[2]').click()
    
    areaChecked=driver.find_element_by_css_selector(area)
    areaText=areaChecked.text
    areaChecked.click()
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
            time.sleep(1)
            
            #검색버튼 클릭
            driver.find_element_by_css_selector('#contents > div.catsearchBox.border.welsearchBox.serviceTypeIn > div.inpWrap > div > fieldset > a').click()
            time.sleep(0.5)
            
            
            #복지정보 추출 
            keyURL='http://bokjiro.go.kr/welInfo/retrieveGvmtWelInfo.do?welInfSno='
            ##가져오기
            listContainer=driver.find_element_by_css_selector('#contents > div.resultBox > ul')
            listItems=listContainer.find_elements_by_tag_name('li')
            
            # #결과 없으면 넘김
            # if not listItems:
            #     #다시 유형 열고
            #     typeParent=driver.find_element_by_xpath('//*[@title="유형 열기"]')
            #     typeParent.click()
            #     #time.sleep(0.5)
            
            #     ul=driver.find_element_by_xpath('//*[@id="contents"]/div[2]/div[1]/div/fieldset/div/div/div/ul')
            #     li=ul.find_elements_by_tag_name('li')
            #     #클릭했던거 해제
            #     theItem=li[domainIndex]
            #     theItem.click()
            #     #time.sleep(0.5)
            #     typeParent.click()
            #     continue
            
            for liIndex in range(len(listItems)):
                #db삽입용 복지 제목, 내용, 링크
                title=listItems[liIndex].find_element_by_tag_name('a').text
                desc=listItems[liIndex].find_element_by_class_name('copy').text
                link=listItems[liIndex].find_element_by_tag_name('a').get_attribute('href')
                link=re.sub(r'[^0-9]', '', link)
                link=keyURL+link
                
                driver2.get(link)
                details=driver2.find_element_by_xpath('//*[@id="contents"]/div[3]/div[1]/..').text
                
                contentIndex=details.find('서비스 내용')
                applyIndex=details.find('서비스 이용 및 신청방법')
                cutIndex=details.find('서식/자료')

                #서비스대상
                target=details[7:contentIndex].rstrip()
                #서비스내용
                content=details[contentIndex+7:applyIndex].rstrip()
                #지원방법
                how=details[applyIndex+14:cutIndex].rstrip()
                
                data={'유형':domain,'지역':areaText,'시/군/구':sggText,'제목':title,'내용':desc,'링크':link,'대상':target,'상세내용':content,'지원방법':how}
                resultList.append(data)

                print('유형:',domain)
                print('지역:',areaText)
                print('시/군/구:',sggText)
                print('타이틀: ',title)
                print('내용:',desc)
                print('링크:',link)
                print('대상:',target)
                print('상세내용:',content)
                print('지원방법:',how)
                print('\n')
                
            """페이지가 하나 이상이면 다음 것들 조회하도록 하는 부분인데
               지자체만 검색하면 결과가 매우 적어서 불필요할 듯하다."""    
            ##다음 페이지 있는지 확인 후 이동
            #nextPages=driver.find_element_by_css_selector('#contents > div.resultBox > div')
            #pages=nextPages.find_elements_by_tag_name('a')
            
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
    df=DataFrame(resultList,columns=['유형','지역','시/군/구','제목','내용','링크','대상','상세내용','지원방법'])
    df.to_csv('./dataset2.csv',mode='a', encoding="utf-8-sig")
    
    driver.quit()
    driver2.quit()
    return

    
if __name__=='__main__':
    pool = Pool(processes=32) # 32개의 프로세스를 사용합니다.
    async_pool=pool.map_async(crawlByArea, areaSelectors) # get_contetn 함수를 넣어줍시다
    
    async_pool.wait()
    
