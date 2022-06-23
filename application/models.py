from application import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    # desc = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False)
    pub_date = db.Column(db.String(64), nullable=False)
    category = db.Column(db.String(12), nullable=False)
