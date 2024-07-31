from backend import db
from datetime import datetime, timedelta


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    role = db.Column(db.String(20), default='user', nullable=False)
    issues = db.relationship('BookIssue', backref='user', lazy=True)
    flag = db.Column(db.Boolean, default=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Section(db.Model):
    __tablename__ = 'sections'
    section_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    books = db.relationship('Book', backref='section', lazy=True)

    def as_dict(self):
        return {col.name: getattr(self, col.name) for col in self.__table__.columns}


class Book(db.Model):
    __tablename__ = 'books'
    book_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('sections.section_id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    language = db.Column(db.String(50), default='English')
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    issues = db.relationship('BookIssue', backref='book', lazy=True)
    available_copies = db.Column(db.Integer, default=1)

    def as_dict(self):
        result = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        if self.date_added:
            result['date_added'] = self.date_added.isoformat()
        return result


class BookIssue(db.Model):
    __tablename__ = 'book_issues'
    issue_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime)
    status = db.Column(db.Enum('requested', 'issued', 'returned'), default='returned', nullable=False)

    def as_dict(self):
        result = {col.name: getattr(self, col.name) for col in self.__table__.columns}
        if self.date_issued:
            result['date_issued'] = self.date_issued.isoformat()
        if self.return_date:
            result['return_date'] = self.return_date.isoformat()
        return result

    def set_return_date(self, duration_days):
        if not self.date_issued:
            self.date_issued = datetime.utcnow()
        self.return_date = self.date_issued + timedelta(days=duration_days)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    feedback_id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    comment = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
