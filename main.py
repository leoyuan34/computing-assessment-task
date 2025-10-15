from flask import Flask, render_template, request, redirect, url_for, session
import database_manager as dbHandler
import time

app = Flask(__name__)
app.secret_key = "transit_travel_tips" 

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("feed"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = dbHandler.verify_user(email, password)
        if user:
            session["user"] = user["username"]
            return redirect(url_for("feed"))
        else:
            return render_template("login.html", error="Invalid credentials.")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        age = request.form["age"]
        email = request.form["email"]
        password = request.form["password"]
        try:
            dbHandler.add_user(username, age, email, password)
            return redirect(url_for("login"))
        except Exception as e:
            print(e)
            return render_template("signup.html", error="Email or username already exists.")
    return render_template("signup.html")
    

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/feed")
def feed():
    posts = dbHandler.get_all_posts()
    
    posts_with_data = []
    for post in posts:
        post_dict = dict(post)
        post_dict['like_count'] = dbHandler.get_post_likes(post['id'])
        post_dict['comment_count'] = dbHandler.get_comment_count(post['id'])
        post_dict['comments'] = dbHandler.get_post_comments(post['id'])
        
        if 'user' in session:
            post_dict['user_has_liked'] = dbHandler.has_user_liked(post['id'], session['user'])
        else:
            post_dict['user_has_liked'] = False
            
        posts_with_data.append(post_dict)
    
    return render_template("feed.html", posts=posts_with_data)

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route('/photography')
def photography():
    return render_template('photography.html')

@app.route('/photography/<continent>')
def continent_photos(continent):
    continent_countries = {
        'africa': ['egypt', 'kenya', 'south-africa', 'morocco', 'tanzania'],
        'asia': ['japan', 'thailand', 'china', 'india', 'vietnam'],
        'europe': ['france', 'italy', 'spain', 'greece', 'uk'],
        'north-america': ['usa', 'canada', 'mexico'],
        'south-america': ['brazil', 'argentina', 'peru', 'chile'],
        'oceania': ['australia', 'new-zealand', 'fiji']
    }
    
    countries = continent_countries.get(continent, [])
    continent_name = continent.replace('-', ' ').title()
    
    return render_template('continent_photos.html', 
                         continent=continent, 
                         continent_name=continent_name,
                         countries=countries)

@app.route('/photography/<continent>/<country>')
def country_photos(continent, country):
    import os
    
    gallery_path = f'static/images/photography/galleries/{country}/'
    photos = []
    
    if os.path.exists(gallery_path):
        photos = [f for f in os.listdir(gallery_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
    
    country_name = country.replace('-', ' ').title()
    continent_name = continent.replace('-', ' ').title()
    
    return render_template('country_photos.html',
                         continent=continent,
                         continent_name=continent_name,
                         country=country,
                         country_name=country_name,
                         photos=photos)

@app.route("/create")
def create():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    posts = dbHandler.get_user_posts(session['user'])
    
    return render_template("create.html", 
                         posts=posts,
                         success=session.pop('success', None),
                         error=session.pop('error', None))

@app.route("/create_post", methods=['POST'])
def create_post():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    title = request.form.get('title')
    content = request.form.get('content')
    username = session['user']
    
    image_path = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename != '':
            import os
            from werkzeug.utils import secure_filename
            
            upload_folder = 'static/images/uploads'
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            
            filename = secure_filename(image.filename)
            timestamp = str(int(time.time()))
            filename = f"{timestamp}_{filename}"
            image.save(os.path.join(upload_folder, filename))
            image_path = f'images/uploads/{filename}'
    
    if dbHandler.create_post(username, title, content, image_path):
        session['success'] = 'Post created successfully!'
    else:
        session['error'] = 'Failed to create post'
    
    return redirect(url_for('create'))

@app.route("/delete_post/<int:post_id>", methods=['POST'])
def delete_post(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if dbHandler.delete_post(post_id, session['user']):
        session['success'] = 'Post deleted successfully'
    else:
        session['error'] = 'Failed to delete post'
    
    return redirect(url_for('create'))

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = dbHandler.get_user_by_username(session['user'])
    user_email = user['email'] if user else ''
    
    return render_template('profile.html', 
                         user_email=user_email,
                         success=session.pop('success', None),
                         error=session.pop('error', None))

@app.route('/update_username', methods=['POST'])
def update_username():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    new_username = request.form.get('new_username')
    old_username = session['user']
    
    existing_user = dbHandler.get_user_by_username(new_username)
    if existing_user and new_username != old_username:
        session['error'] = 'Username already taken'
        return redirect(url_for('profile'))
    
    if dbHandler.update_username(old_username, new_username):
        session['user'] = new_username
        session['success'] = 'Username updated successfully'
    else:
        session['error'] = 'Failed to update username'
    
    return redirect(url_for('profile'))

@app.route('/update_email', methods=['POST'])
def update_email():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    new_email = request.form.get('new_email')
    username = session['user']
    
    if dbHandler.update_email(username, new_email):
        session['success'] = 'Email updated successfully'
    else:
        session['error'] = 'Failed to update email'
    
    return redirect(url_for('profile'))

@app.route('/update_password', methods=['POST'])
def update_password():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    from werkzeug.security import check_password_hash
    
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    username = session['user']
    
    user = dbHandler.get_user_by_username(username)
    if not user or not check_password_hash(user['password'], current_password):
        session['error'] = 'Current password is incorrect'
        return redirect(url_for('profile'))
    
    if new_password != confirm_password:
        session['error'] = 'New passwords do not match'
        return redirect(url_for('profile'))
    
    if dbHandler.update_password(username, new_password):
        session['success'] = 'Password changed successfully'
    else:
        session['error'] = 'Failed to change password'
    
    return redirect(url_for('profile'))

@app.route("/like_post/<int:post_id>", methods=['POST'])
def like_post(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    dbHandler.like_post(post_id, session['user'])
    
    return redirect(request.referrer or url_for('feed'))

@app.route("/comment_post/<int:post_id>", methods=['POST'])
def comment_post(post_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    comment_text = request.form.get('comment_text')
    
    if comment_text and comment_text.strip():
        dbHandler.add_comment(post_id, session['user'], comment_text)
    
    return redirect(request.referrer or url_for('feed'))

if __name__ == "__main__":
    app.run(debug=True)
