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

@app.route('/test')
def test():
    return render_template('test.html')

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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=2000)
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
        print('hi')
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
    id_recv = int(request.form['id_send'])
    values = db.mates.find_one({'matepost_id': id_recv},{'_id': 0});
    return jsonify({'result': 'success', 'values': values})

@app.route('/api/addLink',methods=['GET'])
def api_addLink():
    #
    # like_num = 0
    # links = [
    #     {
    #         'title': '스포츠몰',
    #         'url': 'http://www.mallmall.net/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '헬스기구전문 브랜드 바디엑스',
    #         'url': 'https://www.bodyx.co.kr/goods/goods_list.php?cateCd=098',
    #         'like': like_num
    #     },
    #     {
    #         'title': '헬스기구의 모든 것! 바디스톤',
    #         'url': 'http://bodystone.co.kr/category/%EB%B4%89/378/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '반도스포츠-등산용품, 헬스용품,스포츠용품 전문매장',
    #         'url': 'http://cbsports.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '코헬스코',
    #         'url': 'http://kohealthco.or.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '유연성운동 - EGOJIN',
    #         'url': 'https://egojin.com/product/list.html?cate_no=61',
    #         'like': like_num
    #     },
    #     {
    #         'title': '플러그 피트니스',
    #         'url': 'http://frogfitness.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '해피요가-요가매트,척추건강',
    #         'url': 'https://www.happyyoga.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '헬스프라자',
    #         'url': 'http://www.health-plaza.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '헬스기구 전문 쇼핑몰 Uspo',
    #         'url': 'http://skin-skin9.healthw.cafe24.com/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '젝시믹스 공식 온라인 스토어',
    #         'url': 'https://www.xexymix.com/?gclid=CjwKCAjwx6WDBhBQEiwA_dP8rZLmQV1AC_yv1wbfu2QtyLfQC6rkvKaaOh_-RAbdsjN3An5M6wTMRhoCO0IQAvD_BwE',
    #         'like': like_num
    #     },
    #     {
    #         'title': '안다르',
    #         'url': 'https://andar.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'STL',
    #         'url': 'http://www.beststl.com/?n_media=122875&n_query=%EC%9A%94%EA%B0%80%EB%B3%B5&n_rank=3&n_ad_group=grp-a001-01-000000001003051&n_ad=nad-a001-01-000000127800552&n_keyword_id=nkw-a001-01-000000187839403&n_keyword=%EC%9A%94%EA%B0%80%EB%B3%B5&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkn38fmf4%7Cci%3D0zi00028LAzur26IJ1j2%7Ctr%3Dsa%7Chk%3D3d1d6f9856db00c56d6e8c0a13f1ba00fb49a343',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'Conch Best - 콘치웨어',
    #         'url': 'https://conch.co.kr/product/list.html?cate_no=171&n_media=122875&n_query=%EC%9A%94%EA%B0%80%EB%B3%B5&n_rank=5&n_ad_group=grp-a001-01-000000020657083&n_ad=nad-a001-01-000000129229970&n_keyword_id=nkw-a001-01-000003598375814&n_keyword=%EC%9A%94%EA%B0%80%EB%B3%B5&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkn38g80w%7Cci%3D0za0002yLAzuZFHDxL29%7Ctr%3Dsa%7Chk%3Df4b46b5173fdae252230a71c4d027a692eb67b83',
    #         'like': like_num
    #     },
    #     {
    #         'title': '에이브',
    #         'url': 'https://abefit.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '집에서 운동할 땐 코어바디',
    #         'url': 'https://www.corebody.co.kr/goods/goods_list.php?cateCd=024003&n_media=122875&n_query=%ED%8F%BC%EB%A1%A4%EB%9F%AC&n_rank=8&n_ad_group=grp-a001-01-000000015479548&n_ad=nad-a001-01-000000094405652&n_keyword_id=nkw-a001-01-000002913465061&n_keyword=%ED%8F%BC%EB%A1%A4%EB%9F%AC&n_campaign_type=1&n_ad_group_type=1&NaPm=ct%3Dkn38i68o%7Cci%3D0Am0003ZLAzuVwiFTvn4%7Ctr%3Dsa%7Chk%3Da764124a227c59094666111024863e3df9835805',
    #         'like': like_num
    #     },
    #     {
    #         'title': '슬로우랩 SlowLab',
    #         'url': 'http://www.slowlab.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '이츠데이',
    #         'url': 'https://itsuday.com/',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'FIT 101',
    #         'url': 'https://www.fit101.co.kr/index.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '근육맨 닷컴',
    #         'url': 'http://www.kun6man.com/m/main.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '피트니스 스토어 - 공식온라인몰',
    #         'url': 'https://fitnessstore.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '엑사이더 공식쇼핑몰',
    #         'url': 'https://www.excider.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '룰루레몬',
    #         'url': 'https://www.lululemon.co.kr/women-activities-training/?CID=ps_sem_google_118103568863_kwd-425820605648_c_p_507059514214___%EC%9A%B4%EB%8F%99%EC%9A%A9%ED%92%88&gclid=Cj0KCQjwsLWDBhCmARIsAPSL3_1oYmkFK2V-moYaS-MeOcn_aaMo8hlwsbOPlesKZRXyHydMFium9HQaAiZCEALw_wcB',
    #         'like': like_num
    #     },
    #     {
    #         'title': 'SPOM - 스포츠용품쇼핑몰',
    #         'url': 'https://www.spom.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '스컬피그',
    #         'url': 'https://skullpig.com/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '필케어',
    #         'url': 'https://www.pilcare.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '2XU',
    #         'url': 'https://www.2xu.kr/?gclid=Cj0KCQjwgtWDBhDZARIsADEKwgP58NqP6Nns8CgOr-6HfOYeySJhdk4sSXll_uyh3Lo23XRn3WVMZUIaAnYLEALw_wcB',
    #         'like': like_num
    #     },
    #     {
    #         'title': '뮬라웨어',
    #         'url': 'http://mulawear.com/m/main.html',
    #         'like': like_num
    #     },
    #     {
    #         'title': '호주요가복 브랜드 :: 락웨어',
    #         'url': 'http://rockwear.co.kr/',
    #         'like': like_num
    #     },
    #     {
    #         'title': '메디테이션 공식온라인몰',
    #         'url': 'http://meditations.co.kr/',
    #         'like': like_num
    #     }
    # ]
    # num = 61
    #
    # for link in links:
    #     link = {
    #         'link_id': num,
    #         'link_category': 'fitness_equipment',
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
