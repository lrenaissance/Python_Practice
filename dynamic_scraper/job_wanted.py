from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

def job_scraping():

  p=sync_playwright().start()

  # create browser
  # headless: 브라우저 생성하지만 보여주지는 않음
  browser=p.chromium.launch(headless=False)

  page=browser.new_page()

  page.goto("https://www.wanted.co.kr/search?query=flutter&tab=position")

  '''
  #공부 목적 코드
  #url로 이동
  page.goto("https://www.wanted.co.kr/")

  # 대기 시간 설정(초)
  time.sleep(3)

  # 검색 버튼 누르기
  # css selector를 인자로 넘기기
  # class name을 가진 btn
  # 요소 찾기: locator
  page.click("button.Aside_searchButton__rajGo")

  time.sleep(3)

  # 검색창에 flutter 입력
  page.get_by_placeholder("검색어를 입력해 주세요.").fill("flutter")

  time.sleep(3)

  page.keyboard.down("Enter")

  time.sleep(5)

  page.click("a#search_tab_position")
  '''

  #scroll down
  for x in range(4):
    time.sleep(5)
    page.keyboard.down("End")

  #full html 가져오기
  content=page.content()

  p.stop()

  #화면 캡처
  #page.screenshot(path="screenshot.png")

  soup=BeautifulSoup(content,"html.parser")

  jobs=soup.find_all("div",class_="JobCard_container__REty8")

  jobs_db=[]

  for job in jobs:
    link=f"https://www.wanted.co.kr{job.find('a')['href']}"
    title=job.find("strong",class_="JobCard_title__HBpZf").text
    company_name=job.find("span",class_="JobCard_companyName__N1YrF").text
    reward=job.find("span",class_="JobCard_reward__cNlG5").text
    job={
      "title":title,
      "company_name":company_name,
      "reward":reward,
      "link":link,
    }
    jobs_db.append(job)
  
  return jobs_db


jobs_db=job_scraping()

#file로 만들기
file=open("jobs.csv","w")
writer=csv.writer(file)

#writerow는 list를 필요로 함
#dictionary -> list? .keys(), .values()
writer.writerow(["Title","Company","Reward","Link",])

for job in jobs_db:
  writer.writerow(job.values())