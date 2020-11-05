from project2 import db

# class User(db.Model, UserMixin):
#     user_id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(20), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password = db.Column(db.String(60), nullable=False)

#     def get_id(self):
#            return (self.user_id)

#     def __repr__(self):
#         return f"User('{self.username}', '{self.email}')"