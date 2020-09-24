from flask import render_template, jsonify, flash, redirect, url_for,request,g

from app.forms import LoginForm,RegistrationForm, EditProfileForm,EmptyForm, PostForm, ResetPasswordRequestForm, ResetPasswordForm

from flask_login import login_user, logout_user, current_user, login_required

from app.forms import ResetPasswordRequestForm
from app.email import send_password_reset_email
from app import app, db
from app.model import People, Post
#from app.email import send_password_reset_email

from datetime import datetime
from PIL import Image
import secrets
import os

from flask_babel import gettext, get_locale
from guess_language import guess_language

from flask import jsonify
from app.translate import translate




@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.locale = str(get_locale())


@app.route("/", methods=['POST','GET'])
@app.route("/index", methods=['POST','GET'])
@login_required
def index():
    
    page = request.args.get('page', 1, type=int)
    posts_ = current_user.followed_posts().paginate(page, app.config['POSTS_PER_PAGE'], False)
    
    prev_url = url_for('index', page=posts_.prev_num) if posts_.has_prev else None
    
    next_url = url_for('index', page=posts_.next_num) if posts_.has_next else None
    
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        #print(language)
        
        if language == "UNKNOWN" or len(language)>5:
            language = ""
        
        post = Post(body=form.post.data, author=current_user, language = language)
        db.session.add(post)
        db.session.commit()
        flash(gettext("Your post is now live!"))
        return redirect (url_for("index"))
        
    return render_template("index.html", title="Home Page", posts=posts_.items, form=form, next_url=next_url, prev_url=prev_url)

@app.route("/login", methods= ['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = People.query.filter(People.username== form.username.data).first()
        
        if user is None:
            flash(gettext("User does not exist."))
            return redirect(url_for("login"))
        if not user.check_password(form.password.data):
            flash(gettext("Invalid username or password"))
            return redirect(url_for("login")) 
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        flash(gettext("Login successful."))
        return redirect(next_page or url_for("index"))
    return render_template("login.html", title="Sign In", form = form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/registration", methods=['POST','GET'])
def registration():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = People(username=form.username.data, email =form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(gettext('Registration Successful'))
        return redirect(url_for('login'))
    return render_template('registration.html', title='Registration', form=form)

@app.route("/user/<username>")
@login_required
def user(username):
    user = People.query.filter(People.username == username).first_or_404()
    
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter(Post.user_id == user.id).paginate(page, app.config['POSTS_PER_PAGE'], False)
    
    next_url = url_for('user', username=current_user, page=posts.next_num, posts=posts) if posts.has_next else None
    
    prev_url = url_for('user', username=current_user, page=posts.prev_num, posts=posts) if posts.has_prev else None
    
    image_file = url_for('static', filename='profile_pics/'+ current_user.image)
    
    form = EmptyForm()
    
    return render_template('user.html', user=user, post=posts.items, title='Profile', image_file=image_file, form=form, prev_url= prev_url, next_url=next_url)

def resize_image(form_image):
    img = Image.open(form_image)
    width = 150
    height = 100
    size = (width, height)
    img = img.resize(size)
    return img

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.split(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    img = resize_image(form_picture)
    img.save(picture_path)
    return picture_fn


@app.route("/edit_profile", methods=['POST','GET'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_name = save_picture(form.picture.data)
            current_user.image = picture_name
        current_user.username = form.username.data
        current_user.email =form.email.data
        current_user.about_me = form.about_me.data 
        db.session.commit()
        flash(gettext('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',form=form)



@app.route("/follow/<username>", methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = People.query.filter(People.username == username).first()
        
        if user is None:
            flash(gettext('User is not in our database.'))
            return redirect(url_for('index'))
        if current_user == user:
            return redirect(url_for('user', username=username))
        
        current_user.follow(user)
        db.session.commit()
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
            
        
        

@app.route("/unfollow/<username>", methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = People.query.filter(People.username == username).first()
        
        if user is None:
            flash(gettext('User is not in our database.'))
            return redirect(url_for('index'))
        
        if current_user == user:
            flash("you cannot unfollow yourself.")
            return redirect(url_for('user', username=username))
        
        current_user.unfollow(user)
        db.session.commit()
        return redirect(url_for('user', username=username))
        
    else:
        return redirect(url_for('index'))
    
    
@app.route("/explore", methods=['GET', 'POST'])
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page, app.config['POSTS_PER_PAGE'], False)
    
    prev_url = url_for('explore', page=posts.prev_num) if posts.has_prev else None 
    
    next_url = url_for('explore', page=posts.next_num) if posts.has_next else None
    
    return render_template("index.html", posts=posts.items, title="Explore", next_url=next_url, prev_url=prev_url)




@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = People.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(gettext('Check your email for the instructions to reset your password.'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = People.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(gettext('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route("/translate", methods=['POST'])
@login_required
def translate():
    return jsonify({'text': translate(request.form['text'],
                                     request.form['source_language'],
                                     request.form['dest_language'])
                            })


@app.route("/dummy")
@login_required
def dummy():
    translate("how are you doing this morning?", "en", "sw")
    return jsonify({"hey":"dummy"})
    
    
    













    