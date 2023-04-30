from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = "r@nd0Sk_1"

@app.route('/')
def index():
  return render_template('index.html')


conn = sqlite3.connect('database24.db', check_same_thread=False)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
  
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=80)])
    loginname = StringField('Loginname', [validators.Length(min=4, max=16)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

  
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        loginname = form.loginname.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cursor.execute("INSERT INTO users(name, loginname, password) VALUES(?,?,?)", (name, loginname,password))

        conn.commit()
        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
       loginname = request.form['loginname']
       cursor.execute('UPDATE users SET is_user="TRUE" where loginname = ? ',[loginname])
       conn.commit()
       msg = "User activated successfully"
       cursor.execute("select loginname, is_user from users where is_user='FALSE'")
       rows = cursor. fetchall()
       return redirect(url_for('login'))

@app.route('/group_user', methods=['GET','POST'])
def group_user():
    if request.method == 'POST':
       loginname = request.form['loginname']
       #groupid = request.form['groupid']
       cursor.execute("INSERT INTO group_user(loginname) VALUES(?)",[loginname])
       conn.commit()
       #data2 = ("select group_name from groups where group_id= ?", [groupid])
       #print(data2)
       msg = "You have been successfully added to the group"
       return render_template('welcome.html',msg=msg)
       
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        loginname = request.form['loginname']
        password_candidate = request.form['password']

        result = cursor.execute("SELECT * FROM users WHERE loginname = ?", [loginname])

        if result != 0:
            data = cursor.fetchone()
            password = data['password']

            if sha256_crypt.verify(password_candidate, password):
              
                session['logged_in'] = True
                session['loginname'] = loginname
                if data['is_admin'] == 'TRUE' and data['is_user'] == 'TRUE':

                  flash('Welcome Admin', 'success')
                  cursor.execute("select loginname, is_user from users where is_user='FALSE'")
                  rows = cursor.fetchall()
                  return render_template('admin.html',rows=rows)
                elif data['is_admin'] == 'FALSE' and data['is_user'] == 'TRUE':
                    msg = "Logged in successfully as user!!!"
                    print(session['loginname'])
                    user = session['loginname']
                    return render_template('hello.html', msg=msg,user=user)
                elif data['is_user'] == 'FALSE' and data['is_admin'] == 'FALSE':
                    flash('Account not activated yet!!','success')   
                    return render_template('login.html') 
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
     app.run(debug=True)
  