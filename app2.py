import os
from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from hypercorn.middleware import AsyncioWSGIMiddleware  # ASGI Middleware

# Load environment variables
load_dotenv()

app2 = Flask(__name__)

# Database configuration
app2.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app2.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

db = SQLAlchemy(app2)

# Convert Flask to ASGI for Uvicorn
asgi_app = AsyncioWSGIMiddleware(app2)

# Define BlogPost model
class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    tags = db.Column(db.ARRAY(db.String), nullable=False)
    content_path = db.Column(db.String(255), nullable=False)

    # Convert object to dictionary for serialization
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "date": self.date.strftime("%Y-%m-%d"),
            "tags": self.tags,
            "content_path": self.content_path
        }

@app2.route('/')
def index():
    return redirect(url_for('blog_post', post_id=1))

@app2.route('/blog/')
def blog():
    return redirect(url_for('blog_post', post_id=1))

@app2.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        abort(404)

    with open(f"templates/{post.content_path}", "r", encoding="utf-8") as file:
        content = file.read()

    all_posts = BlogPost.query.filter(BlogPost.id != post_id).all()

    return render_template(
        'blog_post.html',
        post=post.to_dict(),
        content=content,
        allblog=[p.to_dict() for p in all_posts]
    )

@app2.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=True)
