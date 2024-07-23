from flask import Flask, render_template, request
from dynamic_scraper.job_wanted import job_scraping

app=Flask("JobScraper")

#decorator(@)가 함수 바로 위에 있어야지만 해당 주소로 갔을 때 실행됨
@app.route("/")
def home():
  #return 해주면 웹에서 바로 보여줌
  return render_template("home.html",name="duck")

'''
html을 return 하고 싶다면
main.py와 같은 레벨에 'templates'라는 폴더 생성해서 진행(이름 수정X)
'''

@app.route("/search")
def hello():
  keyword=request.args.get("keyword")
  return render_template("search.html", keyword=keyword)

app.run("127.0.0.1", debug=True)