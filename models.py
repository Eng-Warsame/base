from dbs import db
from flask_login import  UserMixin

class Client(UserMixin, db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    clientname = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def to_select2(self):
        return {"id": self.id, "text": self.clientname}


    def to_dict(self):
        return {
            "id": self.id,
            "clientname": self.clientname,
            "email": self.email,
            "status": self.status
        }
    def __repr__(self):
        return f"<Client {self.clientname}>"    

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

    

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    full_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    user_type = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def update(self):
        db.session.commit()
        return self

