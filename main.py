from flask import Flask, request, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:buildablog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = '48957w9875kjsdhfkahsdkj'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    b_title = db.Column(db.String(50))
    blog = db.Column(db.String(600))


    def __init__(self, b_title, blog):
        self.b_title= b_title
        self.blog = blog

def validate_title(b_title):
    if b_title == "":
        return "enter a title"
    else:
        return ""

def validate_blog(blog):
    if blog == "":
        return "please enter a paragraph"
    else:
        return ""



@app.route('/blog', methods=['GET', 'POST'])
def index():

    id = request.args.get('id')
    if id != None:
        info=Blog.query.filter_by(id=id).all()
        return render_template('blog.html', title=info[0].name, blog=info[0], one_post=True)
    else:
        info = Blog.query.all()
        return render_template('blog.html', title="Build A Blog", blogs=data, one_post=False)



@app.route('/newpost', methods=['GET', 'POST'])
def new_blog():
    if request.method == 'POST':
        b_title = request.form.get('b_title')
        blog = request.form.get('blog')
        if validate_title(b_title) or validate_blog(blog) != "":
            return render_template('newpost.html', title="Enter new blog", title_error=blog_name_validate(blog_name), content_error=blog_body_validate(blog_body), old_name=blog_name, old_entry=blog_body)
        else:
            new_blog = Blog(blog_name, blog_body)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id=' + str(new_blog.id))
    else:
        return render_template("newpost.html", title="New One")




if __name__ == '__main__':
    app.run()
