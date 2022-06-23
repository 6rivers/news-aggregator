from flask import render_template, url_for
from application import app
from application.models import News


@app.route('/')
def index():
    category = 'india'
    news = News.query.filter_by(category=category)

    return render_template('index.html', news=news)


@app.route('/news/<category>')
def news(category):
    n = News.query.filter_by(category=category)

    return render_template('index.html', news=n)
