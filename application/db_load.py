import requests
from bs4 import BeautifulSoup
from application import db
from appliction import cred
from appliction.models import News
import re

apiKey = cred.apiKey

# db.session.query(News).delete()
# db.session.commit()
# news_loader1('https://www.yahoo.com/news/rss', 'world', 10)
# news_loader1('https://telugu.hindustantimes.com/rss/andhra-pradesh', 'andhra pradesh', 10)
# news_loader1('https://telugu.hindustantimes.com/rss/telangana', 'telangana', 10)
# news_loader1('https://www.news18.com/rss/india.xml', 'india', 5)
# news_loader1('https://www.newindianexpress.com/Nation/rssfeed/?id=170&getXmlFeed=true', 'india', 5)
# news_loader1('https://www.espncricinfo.com/rss/content/story/feeds/0.xml', 'sports', 5)
# news_loader2('https://newsapi.org/v2/top-headlines', 'cricbuzz', 5)

# Function to load news from various RSS feeds in to database


def news_loader1(url, category, count):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers).content
    soup = BeautifulSoup(response, 'lxml-xml')
    # news_data = []
    items = soup.find_all('item')
    j = 0
    for i in items:
        if j <= count:
            title = i.title.text
            # print(i.description.text)
            link = i.link.text
            try:
                img = i.find('media:content')
                img_url = img['url']
            except TypeError:
                try:
                    img_url = i.image.text
                except:
                    img_url = i.coverImages.text
            # to clean up dates and time format
            pub_date = i.pubDate.text
            TimeRegex = re.compile(r'\dT')
            mo = TimeRegex.findall(pub_date)
            if mo:
                char = 'T'
                idx = pub_date.index(char)
                pub_date = pub_date[:idx]
            else:
                dash = '+'
                try:
                    idx = pub_date.index(dash) - 1
                    pub_date = pub_date[:idx]
                except Exception:
                    pass

            news = News(title=title, url=link,
                        image_url=img_url, pub_date=pub_date, category=category)
            db.session.add(news)

        j = j + 1
    db.session.commit()
    return 'done'


# Function to load News from API NEWS based on keyword
def news_loader2(url, keyword, count):
    # url = 'https://newsapi.org/v2/top-headlines'
    if keyword == 'cricbuzz':
        category = 'sports'
    params = {
        'country': 'in',
        'category': category,
        'q': keyword,
        'sortBy': 'top',
        'apiKey': apiKey
    }
    response = requests.get(url, params=params)
    response = response.json()
    articles = response['articles']
    j = 0
    for i in articles:
        if j < count:
            if i['urlToImage']:
                title = i['title']
                link = i['url']
                img_url = i['urlToImage']
                pub_date = i['publishedAt']
                TimeRegex = re.compile(r'\dT')
                mo = TimeRegex.findall(pub_date)
                if mo:
                    char = 'T'
                    idx = pub_date.index(char)
                    pub_date = pub_date[:idx]
                else:
                    dash = '+'
                    try:
                        idx = pub_date.index(dash) - 1
                        pub_date = pub_date[:idx]
                    except Exception:
                        pass
                news = News(title=title, url=link,
                            image_url=img_url, pub_date=pub_date, category=category)
                db.session.add(news)
        j = j + 1
    db.session.commit()
    return 'done'
