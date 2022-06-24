import requests
from bs4 import BeautifulSoup
from application import db
from application import cred
from application.models import News, Source
import re

apiKey = cred.apiKey

# Source Table
# s1 = Source(name='Yahoo News', image_url='http://l.yimg.com/rz/d/yahoo_news_en-US_s_f_p_168x21_news.png')
# s2 = Source(name='HindustanTimes Telugu', image_url='https://telugu.hindustantimes.com/assets/images/logo-ht.svg')
# s3 = Source(name='News18', image_url='https://images.news18.com/static_news18/pix/ibnhome/news18/news18-logo-xmln.png')
# s4 = Source(name='NewIndianExpress', image_url='https://images.newindianexpress.com/images/FrontEnd/images/new_logo.jpg?w=640&dpr=1.0')
# s5 = Source(name='ESPNCricinfo', image_url='https://wassets.hscicdn.com/static/images/logo.png')
# s6 = Source(name='Cricbuzz', image_url='https://www.cricbuzz.com/images/cb_logo.svg')
# db.session.add(s1)
# db.session.add(s2)
# db.session.add(s3)
# db.session.add(s4)
# db.session.add(s5)
# db.session.add(s6)
# db.session.commit()

# db.session.query(News).delete()
# db.session.commit()
# news_loader1('https://www.yahoo.com/news/rss', 'world', 10, 'Yahoo News')
# news_loader1('https://telugu.hindustantimes.com/rss/andhra-pradesh', 'andhra pradesh', 10, 'HindustanTimes Telugu')
# news_loader1('https://telugu.hindustantimes.com/rss/telangana', 'telangana', 10, 'HindustanTimes Telugu')
# news_loader1('https://www.news18.com/rss/india.xml', 'india', 5, 'News18')
# news_loader1('https://www.newindianexpress.com/Nation/rssfeed/?id=170&getXmlFeed=true', 'india', 5, 'NewIndianExpress')
# news_loader1('https://www.espncricinfo.com/rss/content/story/feeds/0.xml', 'sports', 5, 'ESPNCricinfo')
# news_loader2('https://newsapi.org/v2/top-headlines', 'cricbuzz', 5, 'Cricbuzz')

# Function to load news from various RSS feeds in to database


def news_loader1(url, category, count, source):
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
            # to remove whatever comes after '\dT' 2022-06-24T19:11:16+05:30
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
            s = Source.query.filter_by(name=source).first()
            news = News(title=title, url=link, image_url=img_url,
                        pub_date=pub_date, category=category, news_source=s)
            db.session.add(news)

        j = j + 1
    db.session.commit()
    return 'done'


# Function to load News from API NEWS based on keyword
def news_loader2(url, keyword, count, source):
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
                s = Source.query.filter_by(name=source).first()
                news = News(title=title, url=link,
                            image_url=img_url, pub_date=pub_date, category=category, news_source=s)
                db.session.add(news)
        j = j + 1
    db.session.commit()
    return 'done'
