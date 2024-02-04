# -*- coding: utf-8 -*-
"""
Created on Sun Feb  4 10:45:32 2024

@author: hanee
"""

# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)

class NewsArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)

# Sample RSS feeds
rss_feeds = [
    'https://example.com/rss/feed1.xml',
    'https://example.com/rss/feed2.xml',
    'http://rss.cnn.com/rss/cnn_topstories.rss',
 'http://qz.com/feed',
 'http://feeds.foxnews.com/foxnews/politics',
 'http://feeds.reuters.com/reuters/businessNews',
 'http://feeds.feedburner.com/NewshourWorld',
 'https://feeds.bbci.co.uk/news/world/asia/india/rss.xml'
    # Add more feeds as needed
]

def fetch_articles(feed_url):
    response = requests.get(feed_url)
    soup = BeautifulSoup(response.text, 'xml')  # Assuming RSS is in XML format

    articles = []
    for item in soup.find_all('item'):
        title = item.find('title').text
        content = item.find('description').text
        articles.append({'title': title, 'content': content})
    
    return articles

@app.route('/update')
def update_database():
    for feed in rss_feeds:
        articles = fetch_articles(feed)
        for article in articles:
            new_article = NewsArticle(title=article['title'], content=article['content'], category='Uncategorized')
            db.session.add(new_article)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/')
def index():
    articles = NewsArticle.query.all()
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
