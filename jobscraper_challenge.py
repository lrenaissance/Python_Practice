import requests
from bs4 import BeautifulSoup


# page 개수 받기
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


# web scraping
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

        print(f"Company: {company}")
        print(f"Title: {title}")
        print(f"Job Description: {desc}")
        print(f"Job Link: {get_link}\n")


# scrape https://berlinstartupjobs.com/engineering/
url = "https://berlinstartupjobs.com/engineering/"
total_pages = get_pages(url)

for x in range(total_pages):
    url = f"https://berlinstartupjobs.com/engineering/page/{x+1}"
    scrape_page(url)
    print(f"------------page {x+1} ended---------------\n")

skills = ["python", "typescript", "javascript", "rust"]

# scrape https://berlinstartupjobs.com/skill-areas/python/
# https://berlinstartupjobs.com/skill-areas/typescript/
# https://berlinstartupjobs.com/skill-areas/javascript/
# https://berlinstartupjobs.com/skill-areas/rust/
for skill in skills:
    print(f"---{skill}---")
    url = f"https://berlinstartupjobs.com/skill-areas/{skill}/"
    scrape_page(url)
