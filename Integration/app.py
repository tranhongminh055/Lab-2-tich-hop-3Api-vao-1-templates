# app.py: 
# backend flask - tich hop 3 he thong vao 1 api duy nhat 

from flask import Flask, jsonify, render_template
# import 3 he thong 
from scraper import get_lazada_products
from weather import get_weather
from news import get_news

# tao flask app
app = Flask(__name__, template_folder='../templates')

# api 1 - lay du lieu lazada
@app.route("/api/lazada")
def api_lazada(): 
    """
    khi frontend goi /api/lazada
    -> backend goi scraper.py de lay du lieu 
    -> tra ve json danh sach san pham 
    """
    return jsonify(get_lazada_products())

# api 2 - lay du lieu thoi tiet
@app.route("/api/weather")
def api_weather():
    return jsonify(get_weather())

# api 3 - lay du lieu tin tuc
@app.route("/api/news")
def api_news():
    return jsonify(get_news())

# route trang chu - hien thi dashboard
@app.route("/")
def home():
    return render_template("dashboard.html") # fe nam trong /templates

# chay app
if __name__ == "__main__":
    app.run(debug=True) # debug giup tu reload khi sua code 
    