from flask import Flask, redirect, request, render_template,request, url_for 
from flask import session as login_session
import pyrebase
Config = {

  "apiKey": "AIzaSyCn8HoNRHb8L0ImJGHFrBypXptPporhEiA",

  "authDomain": "maya-s-project.firebaseapp.com",

  "projectId": "maya-s-project",

  "storageBucket": "maya-s-project.appspot.com",

  "messagingSenderId": "612029573400",

  "appId": "1:612029573400:web:0d25e2b402eb9ab950566d",

  "measurementId": "G-WNDX4T2V4Z",
  "databaseURL":"https://maya-s-project-default-rtdb.firebaseio.com/"

}


firebase = pyrebase.initialize_app(Config)
auth = firebase.auth()
db =firebase.database()

app = Flask(  # Create a flask app
    __name__,
    template_folder='templates',  # Name of html file folder
    static_folder='static'  # Name of directory for static files

)
app.config['SECRET_KEY'] = "Your_secret_string"
@app.route('/', methods=['GET', 'POST'])
def mainpage():
    return render_template("mainpage.html")


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_user_with_email_and_password(email,password)
            return redirect(url_for('product.html'))
        except:
            error = "Authentication failed"
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error =""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            user= {"email": request.form['email'],"password": request.form['password'], "phone": request.form['phonenumber']}
            login_session['user'] = auth.create_user_with_email_and_password(email,password)
            db.child("Users").child(login_session['user']['localId']).set(user)
            return redirect(url_for('product'))
        except:
            error=error

    return render_template("signup.html")
    error=error



@app.route('/signout')
def signout():
    login_session['user'] = None
    auth.current_user = None
    return redirect(url_for('mainpage'))



@app.route('/product', methods=['GET', 'POST'])
def product():

    users = db.child("Users").child(login_session['user']['localId']).get().val()

    return render_template("product.html",users=users, user = login_session['user'])

@app.route('/cart/<string:pic>')
def cart(pic):
    return render_template("cart.html", pic = pic)



# Your code should be above

if __name__ == "__main__":  # Makes sure this is the main process
    app.run(debug=True)