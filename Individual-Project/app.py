from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config={
    "apiKey": "AIzaSyAntkKF0lwKAkejfKt3nx8czFAGelIKrPY",
  "authDomain": "project-860fc.firebaseapp.com",
  "projectId": "project-860fc",
  "storageBucket": "project-860fc.appspot.com",
  "messagingSenderId": "721103743143",
  "appId": "1:721103743143:web:9e872be5819676e4ffd382",
  "databaseURL":"https://project-860fc-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db= firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here
@app.route('/', methods=['GET','POST'])
def home():
    return render_template("home.html")


@app.route('/about', methods=['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/services', methods=['GET','POST'])
def services():
    return render_template("services.html")

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method=="POST":
        name = request.form["name"]
        email= request.form["email"]
        petsname = request.form["petsname"]
        yourmessage = request.form["msg"]
        uid=login_session['user']['localId']
        review={"name": name,"email":email,'petsname':petsname, "msg":yourmessage}
        db.child("Reviews").child(uid).set(review)
        return redirect(url_for("reviews"))
    return render_template("contact.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
       email = request.form['email']
       password = request.form['password']
       try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=login_session['user']['localId']
            user={"full_name":request.form["full_name"],"username":request.form["username"],"bio":request.form["bio"]}
            db.child("Users").child(UID).set(user)
            return redirect(url_for('home'))
       except Exception as e:
           error = "Authentication failed"
    return render_template("signup.html")



@app.route('/signin', methods=['GET','POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] =auth.sign_in_with_email_and_password(email,password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")     

@app.route('/logout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('signin'))

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    reviews = db.child("Reviews").get().val()
    return render_template("reviews.html", reviews=reviews)

#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)