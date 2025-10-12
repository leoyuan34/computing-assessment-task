from flask import Flask, render_template, request, redirect, url_for, session
import database_manager as dbHandler

app = Flask(__name__)
app.secret_key = "transit_travel_tips"  # change this!

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
    # You can change this later to show real posts
    return render_template("feed.html")


@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route('/photography')
def photography():
    return render_template('photography.html')

@app.route('/photography/<continent>')
def continent_photos(continent):
    # Define countries for each continent
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
    
    # Get all photos from the country's gallery folder
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
    return render_template("create.html")

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    # Get user email from database
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
    
    # Check if username already exists
    existing_user = dbHandler.get_user_by_username(new_username)
    if existing_user and new_username != old_username:
        session['error'] = 'Username already taken'
        return redirect(url_for('profile'))
    
    # Update username in database
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
    
    # Update email in database
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
    
    # Verify current password
    user = dbHandler.get_user_by_username(username)
    if not user or not check_password_hash(user['password'], current_password):
        session['error'] = 'Current password is incorrect'
        return redirect(url_for('profile'))
    
    # Check if new passwords match
    if new_password != confirm_password:
        session['error'] = 'New passwords do not match'
        return redirect(url_for('profile'))
    
    # Update password
    if dbHandler.update_password(username, new_password):
        session['success'] = 'Password changed successfully'
    else:
        session['error'] = 'Failed to change password'
    
    return redirect(url_for('profile'))

if __name__ == "__main__":
    app.run(debug=True)
