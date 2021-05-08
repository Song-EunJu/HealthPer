from flask import Flask, render_template, jsonify, request
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

# mongoDB
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.sw_project

#크롤링
path = "./chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(path)

keyword = '전신운동'
url = 'https://search.naver.com/search.naver?where=video&sort=rel&view=big&stype=&query='+keyword+'&playtime=1030&period'
driver.get(url)

body = driver.find_element_by_css_selector('body')
for i in range(3):
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)

req = driver.page_source
soup = BeautifulSoup(req, 'html.parser')

# videos = driver.find_element_by_css_selector(".list_square_inner._square_row")
# time.sleep(5)
videos = soup.select("#main_pack > section > div.api_subject_bx._square_type._prs_vdo_grd > div.video_square_list._svp_list > div > div")
i=1
for video in videos:
    twos = video.select('.square_box > .square_wrap.api_ani_send')
    db.videos.find_one
    for tag in twos:
        url = tag.select_one('a')['href']
        img = tag.select_one('a > img')['src']
        title = tag.select_one('.info_area > .info_title._ellipsis > .text._text').text
        print(url, img, title)
        video_info = {
            'video_id':i,
            'video_title': title,
            'video_url': url,
            'video_img':img,
            'ex_category': keyword
        }
        db.videos.insert_one(video_info)
        i+=1

driver.close()
#
#




@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/api/outputUrl',methods=['GET'])
def api_outputUrl():
    values = list(db.videos.find({},{'_id': 0}));
    return jsonify({'result': 'success', 'values': values})

# @app.route('/list')
# def _list():
#     # --------------------------------- [edit] ---------------------------------- #
#     page = request.args.get('page', type=int, default=1)  # 페이지
#     # --------------------------------------------------------------------------- #
#     question_list = Question.query.order_by(Question.create_date.desc())
#     # --------------------------------- [edit] ---------------------------------- #
#     question_list = question_list.paginate(page, per_page=10)
#     # --------------------------------------------------------------------------- #
#     return render_template('exercise/question_list.html', question_list=question_list)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
