from APP import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    admin = Admin.query.get(int(user_id))
    if admin:
        return admin
    return Student.query.get(int(user_id))


class Admin(db.Model, UserMixin):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    role = 'admin'


class Student(db.Model, UserMixin):
    __tablename__ = "students"
    admission_no = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(10), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    class_section =  db.Column(db.String(5), nullable=False)

    role = 'student'

    def get_id(self):
        return str(self.admission_no)





