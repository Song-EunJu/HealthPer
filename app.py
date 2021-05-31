from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from oauth2client.contrib.flask_util import UserOAuth2

# mongoDB
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client.sw_project

# oAuth

# app.config['SECRET_KEY'] = 'LuffyIsLonely'
# app.config['GOOGLE_OAUTH2_CLIENT_SECRETS_FILE'] = 'client_secret_.json'
# app.config['GOOGLE_OAUTH2_CLIENT_ID'] = '653440379691-3bdrvt9m65scj0mgr8hort4eu9c3ghg1.apps.googleusercontent.com'
# app.config['GOOGLE_OAUTH2_CLIENT_SECRET'] = 'rAQeN-jrkM20fyUrE9Np5O5a'
#
# oauth2 = UserOAuth2(app)

# JWT
SECRET_KEY = 'luffy'

import jwt
import datetime
import hashlib

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/mate')
def mate():
    return render_template('mate.html')

@app.route('/mateDetail')
def mateDetail():
    return render_template('mateDetail.html')

@app.route('/postMate')
def postMate():
    return render_template('postMate.html')

@app.route('/recipe')
def recipe():
    return render_template('recipe.html')

@app.route('/postMeal')
def postMeal():
    return render_template('postMeal.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']

    pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

    person = db.user.find_one({'id': id_receive, 'pw': pw_hash})

    if person is not None: #person이 있으면
        payload = {
            'id': id_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=1000)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})

@app.route('/api/register', methods=['POST'])
def api_register():
    id_receive = request.form['id_give']
    pw_receive = request.form['pw_give']
    nick_receive = request.form['nick_give']

    id_already = db.user.find_one({'id': id_receive})
    nick_already = db.user.find_one({'nick':nick_receive})

    if id_already is not None: #id가 있으면
        return jsonify({'result': 'fail_id', 'msg': '이미 있는 아이디입니다'})
    elif nick_already is not None: #닉네임이 있으면
        return jsonify({'result': 'fail_nick', 'msg': '이미 있는 닉네임입니다'})
    else:
        pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()
        db.user.insert_one({'id': id_receive, 'pw': pw_hash, 'nick': nick_receive})
        return jsonify({'result': 'success'})

@app.route('/api/userInfo', methods=['GET'])
def api_userInfo():
    token_receive = request.headers['token_give']

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result':'success','nickname': user['nick']})

    except jwt.ExpiredSignatureError:
        return jsonify({'result':'fail'})

# @app.route('/test')
# @oauth2.required
# def test():
#     if oauth2.has_credentials():
#         print('login OK')
#     else:
#         print('login NO')
#     return render_template('test.html')

@app.route('/api/showLink', methods=['GET'])
def api_showLink():
    youtube_links = list(db.links.find({'link_category':'youtube'}, {'_id': False}).sort('link_like', -1))
    food_links = list(db.links.find({'link_category':'diet_food'}, {'_id': False}).sort('link_like', -1))
    return jsonify({'result': 'success', 'youtube_links': youtube_links, 'food_links':food_links})

@app.route('/api/linkLike', methods=['POST'])
def api_linkLike():
    link_receive = request.form['link_send']

    link = db.links.find_one({'link_title': link_receive})
    new_like = link['link_like'] + 1

    db.mystar.update_one({'link_title': link_receive}, {'$set': {'link_like': new_like}})

    return jsonify({'result': 'success'})

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

@app.route('/api/mateDetail',methods=['POST'])
def api_mateDetail():
    id_recv = request.form['id_send']
    print(id_recv)
    print(type(id_recv))

    values = db.mates.find_one({'matepost_id': id_recv},{'_id': 0});
    return jsonify({'result': 'success', 'values': values})

@app.route('/api/addLink',methods=['GET'])
def api_addLink():
    #1. youtube link
    # like_num = 0
    # links = [
    #     {
    #         'title': '홈트레이닝 배우기 - 땅끄부부',
    #         'url': 'https://www.youtube.com/channel/UCDVQ0yDp7Bu-BxEfelTHL8g',
    #         'like': like_num
    #     },
    #     {
    #         'title': '바벨라토르 홈트레이닝',
    #         'url': 'https://www.youtube.com/channel/UCDVQ0yDp7Bu-BxEfelTHL8g',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'BIGSIS 빅씨스',
    #         'url': 'https://www.youtube.com/c/BIGSIS/videos',
    #         'like': like_num
    #     },
    #     {
    #         'title': '딩고 헬스 / dingo fitness',
    #         'url': 'https://www.youtube.com/c/%EB%94%A9%EA%B3%A0%ED%97%AC%EC%8A%A4dingofitness/videos',
    #         'like': like_num
    #     },
    #     {
    #         'title': '힙으뜸',
    #         'url': 'https://www.youtube.com/channel/UC4yq3FWEWqMvFNFBsV3gbKQ/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'MotherTV',
    #         'url': 'https://www.youtube.com/c/%EC%97%84%EB%A7%88TV/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'Allblanc TV',
    #         'url': 'https://www.youtube.com/c/AllblancTV/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': '에이핏 afit',
    #         'url': 'https://www.youtube.com/channel/UCRGZCFuFCwp2D_YKByrqRfw/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'SmiHomeTraining스미홈트',
    #         'url': 'https://www.youtube.com/channel/UCPVjwwmDpE6f3n9Ck2oaNTw',
    #         'like': like_num
    #     },
    #     {
    #         'title': '삐약스핏[살빼주는 병맛 다이어트 채널]',
    #         'url': 'https://www.youtube.com/channel/UCxWRe2A7LMTEwMBErR4DkgQ',
    #         'like': like_num
    #     },
    #     {
    #         'title': '주말의홈트',
    #         'url': 'https://www.youtube.com/c/weeknd_homt/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': '발레테라핏 Ballet Thera Fit',
    #         'url': 'https://www.youtube.com/channel/UCcmCbG1-TDwpJwosHt8QP5A',
    #         'like': like_num
    #     },
    #     {
    #         'title': '강하나 스트레칭_stretching',
    #         'url': 'https://www.youtube.com/c/%EA%B0%95%ED%95%98%EB%82%98/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'Hbro 길환TV',
    #         'url': 'https://www.youtube.com/c/Hbro%EA%B8%B8%ED%99%98TV/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'Sunny Funny Fitness',
    #         'url': 'https://www.youtube.com/channel/UCTAcO7MyXetuvExV7Lo_L6Q/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': '비타민신지니 VitaminJINY',
    #         'url': 'https://www.youtube.com/c/%EA%B0%95%ED%95%98%EB%82%98/featured',
    #         'like': like_num
    #     },
    #     {
    #         'title': '흥둥이',
    #         'url': 'https://www.youtube.com/channel/UCHVuoHrPWWTD67Ln1jV4Bew',
    #         'like': like_num
    #     },
    #     {
    #         'title': '여리나핏',
    #         'url': 'https://www.youtube.com/channel/UCHVuoHrPWWTD67Ln1jV4Bew',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'DanoTV',
    #         'url': 'https://www.youtube.com/channel/UCxM_KJ601hwrOpjVC07iMVQ',
    #         'like': like_num
    #     },
    #     {
    #         'title': '제이제이살롱드핏',
    #         'url': 'https://www.youtube.com/channel/UCUsfRCHj5U1wAJEJiQpPLPw',
    #         'like': like_num
    #     },
    #     {
    #         'title': '핏블리 FITVELY',
    #         'url': 'https://www.youtube.com/channel/UC3hRpIQ4x5niJDwjajQSVPg',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'SomiFit 소미핏',
    #         'url': 'https://www.youtube.com/user/miseowon',
    #         'like': like_num
    #     },
    #     {
    #         'title': '추언니 Chueonny',
    #         'url': 'https://www.youtube.com/channel/UCdcEpfd6OZzTqRuX9wSFXaQ',
    #         'like': like_num
    #     },
    #     {
    #         'title': '이지은 다이어트 Jiny diet',
    #         'url': 'https://www.youtube.com/channel/UCKEspD9kts44sG5E80kQcjQ',
    #         'like': like_num
    #     },
    #     {
    #         'title': '빵느 Seoyeon',
    #         'url': 'https://www.youtube.com/channel/UCRrZ5RYIalHLiHq5ftzxM6A',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'Chloe Ting',
    #         'url': 'https://www.youtube.com/user/ChloesAddiction',
    #         'like': like_num
    #     },
    #     {
    #         'title': '조싀앤바믜 Josh & Bamui',
    #         'url': 'https://www.youtube.com/channel/UC22gayxEPsQLhZXpHDjS8Qg',
    #         'like': like_num
    #     },
    #     {
    #         'title': '무나홈트 Moona Workout',
    #         'url': 'https://www.youtube.com/channel/UCMA_DTVCzlALpD8hfGmYAlg',
    #         'like': like_num
    #     },
    #     {
    #         'title': '에일린 mind yoga',
    #         'url': 'https://www.youtube.com/channel/UCKmEDAD5k5KFMcY5wvGIeGQ',
    #         'like': like_num
    #     },
    #     {
    #         'title': '요가은YoGaEu',
    #         'url': 'https://www.youtube.com/channel/UCzfoIbslSwEjlFdFRvh3RLg',
    #         'like': like_num
    #     }
    # ]
    # num = 1
    #
    # for link in links:
    #     link = {
    #         'link_id': num,
    #         'link_category': 'youtube',
    #         'link_title': link['title'],
    #         'link_url': link['url'],
    #         'link_like': link['like']
    #     }
    #     db.links.insert_one(link)
    #     num += 1

    # 2. 다이어트 식품 link

    # 2. 다이어트 식품 link
    # like_num = 0
    # links = [
    #     {
    #         'title': '쥬비스 몰 | JUVIS MALL',
    #         'url': 'https://www.juvismall.co.kr/product/join/list.view?utm_source=naver&utm_medium=cpc_sa_pc&utm_term=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&utm_campaign=gen_201224&n_media=27758&n_query=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&n_rank=4&n_ad_group=grp-a001-01-000000019165451&n_ad=nad-a001-01-000000118686675&n_keyword_id=nkw-a001-01-000003396663650&n_keyword=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkmwosu0o%7Cci%3D0yu0002%5FJ6buA1lKU1pX%7Ctr%3Dsa%7Chk%3D54d845f412ab1ffe743468f3d3e8e33269702f35',
    #         'like': like_num
    #     },
    #     {
    #         'title': '바르닭',
    #         'url': 'http://www.barudak.co.kr/?utm_source=naver&utm_medium=sa_pc&utm_campaign=0301_brand&utm_content=diet&utm_term=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&NaPm=ct%3Dkmwotk94%7Cci%3D0z80002HJ6burZwwCLln%7Ctr%3Dsa%7Chk%3D1d92b65509fefe64f30952f724d419c70a5ccb4a',
    #         'like': like_num
    #     },
    #     {
    #         'title': '아임닭 - 닭가슴살 시작은 아임닭',
    #         'url': 'https://www.imdak.com/main/index.php?&utm_source=naver_bs_pc&utm_medium=brand&utm_campaign=main_title&utm_term=%EB%A9%94%EC%9D%B8%ED%83%80%EC%9D%B4%ED%8B%80&utm_content=%EC%83%81%EC%8B%9C%EC%86%8C%EC%9E%AC&_ccam=naver&_ccac=pc&_ccar=%EB%A9%94%EC%9D%B8%ED%83%80%EC%9D%B4%ED%8B%80&_ccar=brand&n_media=27758&n_query=%EC%95%84%EC%9E%84%EB%8B%AD&n_rank=1&n_ad_group=grp-a001-04-000000018422177&n_ad=nad-a001-04-000000121619243&n_keyword_id=nkw-a001-04-000003308192623&n_keyword=%EC%95%84%EC%9E%84%EB%8B%AD&n_campaign_type=4&n_contract=tct-a001-04-000000000345334&n_ad_group_type=5&NaPm=ct%3Dkmwoufw0%7Cci%3D0zS0003kJ6buSnGk5fjn%7Ctr%3Dbrnd%7Chk%3D0cc67b5d6dd74ae783e6fcf1e03fa86ce3b976c1',
    #         'like': like_num
    #     },
    #     {
    #         'title': '헬스앤뷰티 : 국내 헬스푸드 대표',
    #         'url': 'https://www.hnbclub.co.kr/?NaPm=ct%3Dkmwowjxi%7Cci%3Dcheckout%7Ctr%3Dds%7Ctrx%3D%7Chk%3De761a7b784bcf7006a14b7d1e0b484aadd572fcc',
    #         'like': like_num
    #     },
    #     {
    #         'title': '건강한 생각, GRN과 함께해요',
    #         'url': 'http://www.tgrn.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '포켓도시락',
    #         'url': 'http://3care.co.kr/shop/shopbrand.html?xcode=025&type=Y&n_media=27758&n_query=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD&n_rank=1&n_ad_group=grp-a001-01-000000000713283&n_ad=nad-a001-01-000000090627486&n_keyword_id=nkw-a001-01-000000118424869&n_keyword=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkmwp11jk%7Cci%3D0Ae0000%2DJAbu02RT41m3%7Ctr%3Dsa%7Chk%3D3f5913d0a0a8d2947b5d05ebd79c1160ea77788e',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'DANOSHOP - 건강한 식단 전문 쇼핑몰',
    #         'url': 'https://danoshop.net/search/?keywords=%EB%8B%A4%EB%85%B8%ED%95%9C%EB%81%BC%EB%8F%84%EC%8B%9C%EB%9D%BD&utm_campaign=paid_media&utm_source=naver&utm_medium=ad_keyword&utm_content=dosirak_no_all&utm_term=%B4%D9%C0%CC%BE%EE%C6%AE%B5%B5%BD%C3%B6%F4&NaPm=ct%3Dkmwp1pgo%7Cci%3D0zG0000DJAbuqGC6rLmg%7Ctr%3Dsa%7Chk%3Da7a15ce7c9fe2c94ff07ad9db8cf60293d84bcb6',
    #         'like': like_num
    #     },
    #     {
    #         'title': '아임웰 - 나의 식단 플래너',
    #         'url': 'https://www.imwell.com/goods/goods_view.php?goodsNo=1000000379&cosemkid=nc16127715005106104&utm_medium=cpc&utm_campaign=0.%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD_PC&utm_term=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD&NaPm=ct%3Dkmwp2b2g%7Cci%3D0zu00015JAbuqbLXvLlv%7Ctr%3Dsa%7Chk%3D37d4a52d57ecae687ab06136d9c0cf2b30743730',
    #         'like': like_num
    #     },
    #     {
    #         'title': '허벌라이프 뉴트리션 공식 홈페이지 | Herbalife Nutrition KR',
    #         'url': 'https://www.herbalife.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '그리밀 단백질 쉐이크 식사대용 다이어트 파우더 : 그리밀',
    #         'url': 'https://smartstore.naver.com/grimeal/products/2764406013?n_media=27758&n_query=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&n_rank=3&n_ad_group=grp-a001-01-000000006619198&n_ad=nad-a001-01-000000121183738&n_keyword_id=nkw-a001-01-000001228830617&n_keyword=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EC%9D%8C%EC%8B%9D&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkmwp61bs%7Cci%3D0zW0003NJAbuPV%2DswL1N%7Ctr%3Dsa%7Chk%3Dc6123b83b389a05b260891bf56e83bd53f988067',
    #         'like': like_num
    #     },
    #     {
    #         'title': '잇츠리얼 - 건강한 다이어트 전문 쇼핑몰',
    #         'url': 'https://eatsreal.co.kr/47',
    #         'like': like_num
    #     },
    #     {
    #         'title': '바디나인',
    #         'url': 'http://bodynine.com/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '다신샵 공식몰 - 맛있고 건강한 다이어트',
    #         'url': 'http://dshop.dietshin.com/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '휴럼샵 - 대한민국 건강식품 휴럼',
    #         'url': 'https://m.hurumshop.com/main/index.php',
    #         'like': like_num
    #     },
    #     {
    #         'title': '그리팅몰 :: 우리집 밥상주치의',
    #         'url': 'https://www.greating.co.kr/?gclid=CjwKCAjwpKCDBhBPEiwAFgBzj75Yefr98XeC3F906iApvrex60BPH76N2xneVCmMe_5TUGvX2V08PBoCgsQQAvD_BwE',
    #         'like': like_num
    #     },
    #     {
    #         'title': '식단으로 찾는 가치관리, 마이비밀',
    #         'url': 'https://www.google.com/amp/m.mybmeal.co.kr/amp/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '랭킹에 답이 있다 - 랭킹닭컴',
    #         'url': 'https://m.rankingdak.com/?gclid=CjwKCAjwpKCDBhBPEiwAFgBzj5Kv-ZaI2mZaYv_iBPbbWNJt0Gt8tV6viulJRW5jhFevy8rCyaY5uBoCMjYQAvD_BwE',
    #         'like': like_num
    #     },
    #     {
    #         'title': '슬림쿡 몸매관리',
    #         'url': 'http://www.slimcook.co.kr/html/mainm.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '미트리 공식쇼핑몰 || metree',
    #         'url': 'https://metree.co.kr/index/index.php?sponsor=&refere=',
    #         'like': like_num
    #     },
    #     {
    #         'title': '뉴트리온',
    #         'url': 'https://m.nutrione.co.kr/goods/goods_list.php?cateCd=018',
    #         'like': like_num
    #     },
    #     {
    #         'title': '허닭',
    #         'url': 'http://www.heodak.com/m/product_list.html?type=M&xcode=010&mcode=007',
    #         'like': like_num
    #     },
    #     {
    #         'title': '하트너뉴트리션',
    #         'url': 'https://m.heartener.kr/product/list.html?cate_no=45',
    #         'like': like_num
    #     },
    #     {
    #         'title': '모여라몰',
    #         'url': 'https://moyeo-ra.co.kr/main/index',
    #         'like': like_num
    #     },
    #     {
    #         'title': '데일리밀 [저염식 도시락 배달]',
    #         'url': 'http://www.thedailymeal.co.kr/?n_media=122875&n_query=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD&n_rank=16&n_ad_group=grp-m001-01-000001435054659&n_ad=nad-a001-01-000000037413763&n_keyword_id=nkw-a001-01-000000837861933&n_keyword=%EB%8B%A4%EC%9D%B4%EC%96%B4%ED%8A%B8%EB%8F%84%EC%8B%9C%EB%9D%BD&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkncoo23c%7Cci%3D0zy0003dtB9usVdDNvi2%7Ctr%3Dsa%7Chk%3Dca1833068ef0d6a96a1cf8eb5c154f281c81c7e2',
    #         'like': like_num
    #     },
    #     {
    #         'title': '바디밥스 다이어트도시락',
    #         'url': 'https://www.bodycreator.co.kr/?NaPm=ct%3Dkncop3wg%7Cci%3D0yC00000tR9ukp4Jz1nu%7Ctr%3Dsa%7Chk%3Daa680d4e0486b25b926acf88d43c0665835d8aff',
    #         'like': like_num
    #     },
    #     {
    #         'title': '잇슬림 - 오늘의 나를 위한 잇슬림',
    #         'url': 'http://www.eatsslim.co.kr/index_es.jsp',
    #         'like': like_num
    #     },
    #     {
    #         'title': '프레시온 FRESH ON',
    #         'url': 'http://fresh-on.co.kr/main/index.php',
    #         'like': like_num
    #     },
    #     {
    #         'title': '바스락',
    #         'url': 'http://basrak.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '착한부자 다이어트 도시락',
    #         'url': 'http://a-good-rich-man.com/index.php',
    #         'like': like_num
    #     },
    #     {
    #         'title': '러브잇',
    #         'url': 'https://love-eat.co.kr/',
    #         'like': like_num
    #     }
    # ]
    # num = 1
    #
    # for link in links:
    #     link = {
    #         'link_id': num,
    #         'link_category': 'diet_food',
    #         'link_title': link['title'],
    #         'link_url': link['url'],
    #         'link_like': link['like']
    #     }
    #     db.links.insert_one(link)
    #     num += 1


    return jsonify({'result': 'success'})

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

@app.route('/api/postMeal', methods=['POST'])
def api_postMeal():
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
