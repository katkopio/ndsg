from project2 import db

class GPXFile(db.Model):
    file_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(60), unique=False, nullable=False)
