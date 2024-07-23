from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

#web3
def web3_scrape(keyword):
  print("scraping web3.career...")
  url=f"https://web3.career/{keyword}-jobs"
  response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
  
  soup=BeautifulSoup(response.content, "html.parser",)

  jobs=soup.find("tbody", class_="tbody").find_all("tr")
  
  all_jobs=[]
  
  for job in jobs:
    h2=job.find("h2", class_="my-primary")
    if h2:
        title = h2.text.strip()
    else:
        continue
    #company=job.find("td",class_="job-location-mobile").text
    company=job.find("h3")
    if company:
        company=company.text.strip()
    else:
        continue
    
    link=job.find('a')["href"]
    
    job_data={
      "title":title,
      "company":company,
      "link":f"https://web3.career/{link}"
    }
    
    all_jobs.append(job_data)
  return all_jobs
# berlin startup
def get_pages(url):
    response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })

    soup = BeautifulSoup(response.content, "html.parser")
    pages = soup.find("ul",
                      class_="bsj-nav").find_all(class_="page-numbers")[0:-1]

    return len(pages)

# berlin startup
def scrape_page(url):
    response = requests.get(
        url,
        headers={
            "User-Agent":
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        })
    soup = BeautifulSoup(
        response.content,
        "html.parser",
    )

    jobs = soup.find("ul", class_="jobs-list-items").find_all("li")
    all_jobs=[]
    
    for job in jobs:
        # featured는 제거
        if 'bjs-jlid__is-featured' in job.get('class', []):
            continue
        # company, title, desc, link
        company = job.find("a", class_="bjs-jlid__b").text
        title = job.find("a").text
        desc = job.find("div", class_="bjs-jlid__description").text

        link = job.find("a")["href"]
        # 현재 화면에서 job 화면으로 넘어가서 버튼 링크 찾기
        response_link = requests.get(
            link,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
        soup_link = BeautifulSoup(
            response_link.content,
            "html.parser",
        )
        get_link = soup_link.find(
            "div", class_="bsj-template__actions").find("a")["href"]
        
        job_data={
        "title":title,
        "company":company,
        "link":get_link,
        }
        
        all_jobs.append(job_data)
    return all_jobs

#berlin startup
def berlin_startup_scrape(keyword):
    print("scraping berlinstartupjobs.com...")
    url = "https://berlinstartupjobs.com/engineering/"
    total_pages = get_pages(url)
    
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    all_jobs=scrape_page(url)
    return all_jobs

#weworkremotely
def wwr_scrape(keyword):
    print("scraping weworkremotely.com...")
    url=f"https://weworkremotely.com/remote-jobs/search?utf8=%E2%9C%93&term={keyword}"
    response = requests.get(
            url,
            headers={
                "User-Agent":
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            })
    
    soup=BeautifulSoup(response.content, "html.parser",)

    jobs=soup.find_all("li")
    
    all_jobs=[]
    
    for job in jobs:
        title=job.find("span",class_="title")
        if title:
            title=title.text
            #print(title)
        else:
            continue
            
        company=job.find("span",class_="company")
        if company:
            company=company.text
            #print(company)
        else:
            continue
        
        link=job.find_all("a")[1]["href"]
        
        job_data={
        "title":title,
        "company":company,
        "link":f"https://weworkremotely.com{link}",
        }
        all_jobs.append(job_data)
    
    return all_jobs
        

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
  keyword=request.args.get("keyword")
  web3=web3_scrape(keyword)
  berlin=berlin_startup_scrape(keyword)
  wwr=wwr_scrape(keyword)
  jobs=web3+berlin+wwr
  return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run()