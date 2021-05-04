from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient('localhost', 27017)

db = client.sw_project

# keyword = '전신운동'
# req = requests.get('https://www.google.com/search?q='+keyword)
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')

# url = soup.select('.g')
# for urll in url:
#     a_tag = urll.select_one('#rso > div:nth-child(4) > div > div > div.yuRUbf > a')
#     print(a_tag)
# # @app.route('/')

# def home():
#     return render_template('index.html');
#
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/exercise')
def exercise():
    return render_template('exercise.html')

@app.route('/api/inputUrl',methods=['POST'])
def api_inputUrl():
    id_receive = request.form['id']
    url = {
        'video_id':3,
        'video_title':'전신운동3',
        'video_url':'https://www.youtube.com/watch?v=swRNeYw1JkY',
        'ex_category':'전신'
    }
    db.videos.insert_one(url)
    return jsonify({'result': 'success', })

@app.route('/api/outputUrl',methods=['GET'])
def api_outputUrl():
    values = list(db.videos.find({},{'_id': 0}));
    return jsonify({'result': 'success', 'values': values})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
