from application import db


class Source(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    image_url = db.Column(db.Text)
    news = db.relationship('News', backref='news_source', lazy='dynamic')


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    # desc = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(12), nullable=False)
    source_id = db.Column(db.Integer, db.ForeignKey('source.id'))
