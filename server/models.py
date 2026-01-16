from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model, SerializerMixin):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String)

    posts = db.relationship('Post', backref='author')

    @validates('name')
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Author must have a name")

        existing = Author.query.filter(Author.name == value).first()
        if existing:
            raise ValueError("Author name must be unique")

        return value

    @validates('phone_number')
    def validate_phone(self, key, value):
        if value and (not value.isdigit() or len(value) != 10):
            raise ValueError("Phone number must be exactly ten digits")
        return value


class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    summary = db.Column(db.String)
    content = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'))

    @validates('content')
    def validate_content(self, key, value):
        if not value or len(value) < 250:
            raise ValueError("Content must be at least 250 characters")
        return value

    @validates('summary')
    def validate_summary(self, key, value):
        if value and len(value) > 250:
            raise ValueError("Summary must be 250 characters or less")
        return value

    @validates('category')
    def validate_category(self, key, value):
        if value not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category must be Fiction or Non-Fiction")
        return value

    @validates('title')
    def validate_title(self, key, value):
        clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(word in value for word in clickbait):
            raise ValueError("Title must be clickbait-y")
        return value
