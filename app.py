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

# #크롤링
# path = "./chromedriver_win32/chromedriver.exe"
# driver = webdriver.Chrome(path)
# 
# keyword = '하체운동'
# url = 'https://search.naver.com/search.naver?where=video&sort=rel&view=big&stype=&query='+keyword+'&playtime=1030&period'
# driver.get(url)
#
# body = driver.find_element_by_css_selector('body')
# for i in range(3):
#     body.send_keys(Keys.PAGE_DOWN)
#     time.sleep(1)
#
# req = driver.page_source
# soup = BeautifulSoup(req, 'html.parser')
#
# videos = driver.find_element_by_css_selector(".list_square_inner._square_row")
# time.sleep(5)
# videos = soup.select("#main_pack > section > div.api_subject_bx._square_type._prs_vdo_grd > div.video_square_list._svp_list > div > div")
# events = list(db.videos.find({}, {'_id': 0}));
# i=len(events)+1
# for video in videos:
#     twos = video.select('.square_box > .square_wrap.api_ani_send')
#
#     for tag in twos:
#         url = tag.select_one('a')['href']
#         img = tag.select_one('a > img')['src']
#         title = tag.select_one('.info_area > .info_title._ellipsis > .text._text').text
#         print(url, img, title)
#         video_info = {
#             'video_id':i,
#             'video_title': title,
#             'video_url': url,
#             'video_img':img,
#             'ex_category': keyword
#         }
#         db.videos.insert_one(video_info)
#         i+=1
#
# driver.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/mate')
def mate():
    return render_template('mate.html')

@app.route('/postMate')
def postMate():
    return render_template('postMate.html')

@app.route('/api/getCategory',methods=['POST'])
def api_getCategory():
    category_recv = request.form['category_send']
    if category_recv == '전체보기':
        exercises = list(db.videos.find({}, {'_id': 0}));
    else:
        exercises = list(db.videos.find({'ex_category': category_recv},{'_id': 0})); # {_id : 0}은 원하지 않는 필드를 제외하는 것
    return jsonify({'result': 'success', 'exercises': exercises})

@app.route('/api/getAll',methods=['GET'])
def api_getAll():
    # page = request.args.get('page',1,type=int)
    values = list(db.videos.find({},{'_id': 0}));
    return jsonify({'result': 'success', 'values': values})

# @app.route('/api/addLink',methods=['POST'])
# def api_addLink():
#     links = [
#         {
#             title: '홈트레이닝 배우기 - 땅끄부부',
#             url: 'https://www.youtube.com/channel/UCDVQ0yDp7Bu-BxEfelTHL8g',
#         },
#         {
#             title: '바벨라토르 홈트레이닝',
#             url: 'https://www.youtube.com/channel/UCDVQ0yDp7Bu-BxEfelTHL8g'
#         },
#         {
#             title: 'BIGSIS 빅씨스',
#             url: 'https://www.youtube.com/c/BIGSIS/videos',
#         },
#         {
#             title: '딩고 헬스 / dingo fitness',
#             url: 'https://www.youtube.com/c/%EB%94%A9%EA%B3%A0%ED%97%AC%EC%8A%A4dingofitness/videos',
#         },
#         {
#             title: '힙으뜸',
#             url: 'https://www.youtube.com/channel/UC4yq3FWEWqMvFNFBsV3gbKQ/featured',
#         },
#         {
#             title: 'MotherTV',
#             url: 'https://www.youtube.com/c/%EC%97%84%EB%A7%88TV/featured',
#         },
#         {
#             title: 'Allblanc TV',
#             url: 'https://www.youtube.com/c/AllblancTV/featured',
#         },
#         {
#             title: '에이핏 afit',
#             url: 'https://www.youtube.com/channel/UCRGZCFuFCwp2D_YKByrqRfw/featured',
#         },
#         {
#             title: 'SmiHomeTraining스미홈트',
#             url: 'https://www.youtube.com/channel/UCPVjwwmDpE6f3n9Ck2oaNTw',
#         },
#         {
#             title: '삐약스핏[살빼주는 병맛 다이어트 채널]',
#             url: 'https://www.youtube.com/channel/UCxWRe2A7LMTEwMBErR4DkgQ',
#         },
#         {
#             title: '주말의홈트',
#             url: 'https://www.youtube.com/c/weeknd_homt/featured',
#         },
#         {
#             title: '발레테라핏 Ballet Thera Fit',
#             url: 'https://www.youtube.com/channel/UCcmCbG1-TDwpJwosHt8QP5A',
#         },
#         {
#             title: '강하나 스트레칭_stretching',
#             url: 'https://www.youtube.com/c/%EA%B0%95%ED%95%98%EB%82%98/featured',
#         },
#         {
#             title: 'Hbro 길환TV',
#             url: 'https://www.youtube.com/c/Hbro%EA%B8%B8%ED%99%98TV/featured',
#         },
#         {
#             title: 'Sunny Funny Fitness',
#             url: 'https://www.youtube.com/channel/UCTAcO7MyXetuvExV7Lo_L6Q/featured',
#         },
#         {
#             title: '비타민신지니 VitaminJINY',
#             url: 'https://www.youtube.com/c/%EA%B0%95%ED%95%98%EB%82%98/featured',
#         },
#         {
#             title: '흥둥이',
#             url: 'https://www.youtube.com/channel/UCHVuoHrPWWTD67Ln1jV4Bew',
#         },
#         {
#             title: '여리나핏',
#             url: 'https://www.youtube.com/channel/UCHVuoHrPWWTD67Ln1jV4Bew',
#         },
#         {
#             title: 'DanoTV',
#             url: 'https://www.youtube.com/channel/UCxM_KJ601hwrOpjVC07iMVQ',
#         },
#         {
#             title: '제이제이살롱드핏',
#             url: 'https://www.youtube.com/channel/UCUsfRCHj5U1wAJEJiQpPLPw',
#         },
#         {
#             title: '핏블리 FITVELY',
#             url: 'https://www.youtube.com/channel/UC3hRpIQ4x5niJDwjajQSVPg',
#         },
#         {
#             title: 'SomiFit 소미핏',
#             url: 'https://www.youtube.com/user/miseowon',
#         },
#         {
#             title: '추언니 Chueonny',
#             url: 'https://www.youtube.com/channel/UCdcEpfd6OZzTqRuX9wSFXaQ',
#         },
#         {
#             title: '이지은 다이어트 Jiny diet',
#             url: 'https://www.youtube.com/channel/UCKEspD9kts44sG5E80kQcjQ',
#         },
#         {
#             title: '빵느 Seoyeon',
#             url: 'https://www.youtube.com/channel/UCRrZ5RYIalHLiHq5ftzxM6A',
#         },
#         {
#             title: 'Chloe Ting',
#             url: 'https://www.youtube.com/user/ChloesAddiction',
#         },
#         {
#             title: '조싀앤바믜 Josh & Bamui',
#             url: 'https://www.youtube.com/channel/UC22gayxEPsQLhZXpHDjS8Qg',
#         },
#         {
#             title: '무나홈트 Moona Workout',
#             url: 'https://www.youtube.com/channel/UCMA_DTVCzlALpD8hfGmYAlg',
#         },
#         {
#             title: '에일린 mind yoga',
#             url: 'https://www.youtube.com/channel/UCKmEDAD5k5KFMcY5wvGIeGQ',
#         },
#         {
#             title: '요가은YoGaEu',
#             url: 'https://www.youtube.com/channel/UCzfoIbslSwEjlFdFRvh3RLg'
#         }
#     ]
#     num = 1
#     for i in links:
#         link = {
#             'link_id': num,
#             'link_category': 'youtube',
#             'link_title': i,
#             'link_url': i['url']
#         }
#         db.link.insert_one(link)
#         num+=1
#
#     return jsonify({'result': 'success'})

# @app.route('/api/postMate', methods=['POST'])
# def api_postMate():
#     category_recv = request.form['category_send']
#     age_recv = request.form['age_send']
#     num_recv = request.form['num_send']
#     gender_recv = request.form['gender_send']
#
#     option = {
#         'category': category_recv,
#         'age': age_recv,
#         'num': num_recv,
#         'gender': gender_recv
#     }
#     db.mates.insert_one(option)
#
#     return jsonify({'result': 'success'})


@app.route('/api/searchMate',methods=['POST'])
def api_searchMate():
    category_recv = request.form['category_send']
    age_recv = int(request.form['age_send'])
    num_recv = int(request.form['num_send'])
    gender_recv = request.form['gender_send']

    values = list(db.mates.find({'mate_category': category_recv, 'age': age_recv, 'people_num': {"$lte": num_recv}, 'gender': gender_recv},{'_id': 0}));
    return jsonify({'result': 'success', 'values': values})

@app.route('/api/getMate',methods=['GET'])
def api_getMate():
    matePosts = list(db.mates.find({},{'_id': 0}));
    return jsonify({'result': 'success', 'matePosts': matePosts})

@app.route('/api/postMate', methods=['POST'])
def api_postMate():
    title_recv = request.form['title_send']
    category_recv = request.form['category_send']
    gender_recv = request.form['gender_send']
    age_recv = int(request.form['age_send'])
    num_recv = int(request.form['num_send'])
    start_recv = request.form['start_send']
    due_recv = request.form['due_send']
    detail_recv = request.form['detail_send']
    current_num = 0

    if (db.mates.count()) == 0:
        matepost_id = 1
    else:
        matepost_id = db.mates.count()+1

    if category_recv == '축구':
        mate_image = "https://littledeep.com/wp-content/uploads/2020/09/soccer-illustration-png1.png"
    elif category_recv == '러닝':
        mate_image = "https://imagescdn.gettyimagesbank.com/500/19/416/513/0/1156415598.jpg"
    elif category_recv == '필라테스':
        mate_image = "https://imagescdn.gettyimagesbank.com/500/201905/jv11365924.jpg"
    elif category_recv == '요가':
        mate_image = "https://i.pinimg.com/564x/e6/7e/5d/e67e5da4d36ce49f16604d7ca9922505.jpg"
    elif category_recv == '배드민턴':
        mate_image = "https://i.pinimg.com/564x/45/ad/9e/45ad9ea38cc8d8c8c7332f7068fe1ce3.jpg"
    elif category_recv == '족구':
        mate_image = "https://img-premium.flaticon.com/png/512/606/606668.png?token=exp=1621494558~hmac=445a240856e6d01a2a933de3684e7145"
    elif category_recv == '농구':
        mate_image = "https://littledeep.com/wp-content/uploads/2020/09/basketball-illustration-png1.png"
    elif category_recv == '자전거':
        mate_image = "https://i.pinimg.com/564x/a7/54/c8/a754c8f67d3cc93f3e77248764ee778a.jpg"
    elif category_recv == '탁구':
        mate_image = "https://imagescdn.gettyimagesbank.com/500/201905/jv11365926.jpg"
    elif category_recv == '테니스':
        mate_image = "https://i.pinimg.com/564x/f0/7d/40/f07d408d27f1b6f095c181345ff7f2cb.jpg"

    option = {
        'matepost_id': matepost_id,
        'mate_title': title_recv,
        'mate_category': category_recv,
        'gender': gender_recv,
        'age': age_recv,
        'people_num': num_recv,
        'current_num': current_num,
        'start_date': start_recv,
        'due_date': due_recv,
        # 'address': address_recv,
        'mate_detail': detail_recv,
        'mate_image': mate_image

    }
    db.mates.insert_one(option)

    return jsonify({'result': 'success'})


# # @app.route('/list')
# # def _list():
# #     # --------------------------------- [edit] ---------------------------------- #
# #     page = request.args.get('page', type=int, default=1)  # 페이지
# #     # --------------------------------------------------------------------------- #
# #     question_list = Question.query.order_by(Question.create_date.desc())
# #     # --------------------------------- [edit] ---------------------------------- #
# #     question_list = question_list.paginate(page, per_page=10)
# #     # --------------------------------------------------------------------------- #
# #     return render_template('exercise/question_list.html', question_list=question_list)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
