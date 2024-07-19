#pip install requests
import requests
from bs4 import BeautifulSoup

all_jobs=[]

# 페이지 처리
def scrape_page(url):
  print(f"Scraping {url}...")
  response=requests.get(url)
  
  soup=BeautifulSoup(response.content, "html.parser",)

  # _class: class 자체가 예약어라서 class를 사용하려면 뒤에 _로 구분
  # find_all: 다 집어오기
  # [1:-1]: 불필요한 정보 리스트에서 제외
  jobs=soup.find("section", class_="jobs").find_all("li")[1:-1]

  for job in jobs:
    # class가 title인 span 태그
    title=job.find("span", class_="title").text
    #region=job.find("span", class_="region").text
    region = job.find("span", class_="region").text if job.find( "span", class_="region") else "Region not found"

    # _: ignore
    company,position=job.find_all("span", class_="company")[0:2]

    try:
      url = job.find('div', class_ = 'tooltip--flag-logo').next_sibling['href']
    except KeyError:
      url = 'You need log-in'    
    
    job_data={
      "title":title,
      "company":company.text,
      "position":position.text,
      "region":region,
      "url":f"https://weworkremotely.com{url}",
    }
    
    all_jobs.append(job_data)

def get_pages(url):
  response=requests.get(url)

  soup=BeautifulSoup(response.content,"html.parser")

  return len(soup.find("div",class_="pagination").find_all("span",class_="page",))
    



url="https://weworkremotely.com/categories/remote-full-stack-programming-jobs"

total_pages=get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for x in range(total_pages):
    url=f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    scrape_page(url)

# print(len(all_jobs))