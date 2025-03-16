import os
from flask import Flask, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from hypercorn.middleware import AsyncioWSGIMiddleware  # ASGI Middleware

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database configuration with default fallback
database_url = os.getenv("DATABASE_URL", "postgresql://bloguser:bloguser17899@db:5432/blogdb")
app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS", "False").lower() in ["true", "1"]

db = SQLAlchemy(app)

# Convert Flask to ASGI for Hypercorn/Uvicorn
asgi_app = AsyncioWSGIMiddleware(app)

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

# Ensure database tables are created before the first request
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return redirect(url_for('blog_post', post_id=1))

@app.route('/blog/')
def blog():
    return redirect(url_for('blog_post', post_id=1))

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get(post_id)
    if post is None:
        abort(404)

    try:
        with open(f"templates/{post.content_path}", "r", encoding="utf-8") as file:
            content = file.read()
    except FileNotFoundError:
        abort(404)

    all_posts = BlogPost.query.filter(BlogPost.id != post_id).all()

    return render_template(
        'blog_post.html',
        post=post.to_dict(),
        content=content,
        allblog=[p.to_dict() for p in all_posts]
    )

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# Run the application with Hypercorn
if __name__ == "__main__":
    import hypercorn.asyncio
    hypercorn.asyncio.run("app:asgi_app", bind="0.0.0.0:5000")


# import os
# from flask import Flask, render_template, redirect, url_for, abort
# from flask_sqlalchemy import SQLAlchemy
# from dotenv import load_dotenv
# from hypercorn.middleware import AsyncioWSGIMiddleware  # ASGI Middleware

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)

# # Database configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

# db = SQLAlchemy(app)

# # Convert Flask to ASGI for Uvicorn
# asgi_app = AsyncioWSGIMiddleware(app)

# # Define BlogPost model
# class BlogPost(db.Model):
#     __tablename__ = "blog_posts"
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255), nullable=False)
#     author = db.Column(db.String(100), nullable=False)
#     date = db.Column(db.Date, nullable=False)
#     tags = db.Column(db.ARRAY(db.String), nullable=False)
#     content_path = db.Column(db.String(255), nullable=False)

#     # Convert object to dictionary for serialization
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "title": self.title,
#             "author": self.author,
#             "date": self.date.strftime("%Y-%m-%d"),
#             "tags": self.tags,
#             "content_path": self.content_path
#         }

# @app.route('/')
# def index():
#     return redirect(url_for('blog_post', post_id=1))

# @app.route('/blog/')
# def blog():
#     return redirect(url_for('blog_post', post_id=1))

# @app.route('/blog/<int:post_id>')
# def blog_post(post_id):
#     post = BlogPost.query.get(post_id)
#     if post is None:
#         abort(404)

#     with open(f"templates/{post.content_path}", "r", encoding="utf-8") as file:
#         content = file.read()

#     all_posts = BlogPost.query.filter(BlogPost.id != post_id).all()

#     return render_template(
#         'blog_post.html',
#         post=post.to_dict(),
#         content=content,
#         allblog=[p.to_dict() for p in all_posts]
#     )

# @app.errorhandler(404)
# def page_not_found(error):
#     return render_template('404.html'), 404

# # if __name__ == '__main__':
# #     import uvicorn
# #     uvicorn.run("app:asgi_app", host="0.0.0.0", port=5000, reload=True)
