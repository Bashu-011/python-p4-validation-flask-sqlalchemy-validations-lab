from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

# Add validators
    @validates('name')
    def validate_name(self, key, author_name):
        if author_name is None or author_name == "":

            raise ValueError("Author name is empty")
        
        return author_name
    

    def unique_name(self, key, author_name):

        if Author.query.filter_by(name=author_name).first() is not None:
            raise ValueError("Author name must be unique")
        
        return author_name
    
    @validates('phone_number')
    def number_len(self, key, number):
        if not number.isdigit() or len(number) != 10:
            raise ValueError("Phone number exceeds 10 digits")
        
        return number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    @validates('content')
    def len_content(self, key, content):
        if len(content) < 250:
            raise ValueError('Content is less than 250 characters')
        return content
    
    @validates('summary')
    def len_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError('Summary is more than 250 characters')
        return summary
    
    @validates('category')
    def post_category(self, key, category):
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Category should be Fiction or Non-Fiction")
        return category
    
    @validates('title')
    def clickbait(self, key, title):
        clickbait = ["Won't Believe", "Secret", "Top" ,"Guess"]
        if not any(word in title for word in clickbait):
            raise ValueError("The title is not clicknbait-y enough")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
