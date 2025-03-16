from flask import Flask, render_template, url_for, redirect, abort
import json
import os


app = Flask(__name__)

with open('blogdata/blogdata.json', 'r', encoding='utf-8') as file:
    blog_data = json.load(file)

@app.route('/')
def index():
    return redirect(url_for('blog_post', post_id=1))

@app.route('/blog/')
def blog():
    return redirect(url_for('blog_post', post_id=1))

@app.route('/<int:post_id>/')
def blog_redirect(post_id):
    return redirect(url_for('blog_post', post_id=post_id))

@app.route('/blog/<int:post_id>')
def blog_post(post_id):
    with open('blogdata/blogdata.json', 'r', encoding='utf-8') as file:
        blog_data = json.load(file)
    post = next((p for p in blog_data['blog_posts'] if p['id'] == post_id), None)
    
    if post is None:
        abort(404)
    
    with open(f"templates/{post['content_path']}", "r", encoding="utf-8") as file:
        data = file.read()
    
    blog_data['blog_posts'].remove(post)
        
    return render_template('blog_post.html', post=post, content=data, allblog=blog_data['blog_posts'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
