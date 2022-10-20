from flask import *
from flask_session import Session
from flask_mail import Mail, Message
import requests
from secrets import token_urlsafe
import json 
from pathlib import Path
import os

app = Flask(__name__)
path = str(Path(__file__).parent) + '/'
print(path)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configuration of mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'snehashish.laskar@sahyadrischool.orf'
app.config['MAIL_PASSWORD'] = 'snehashish08036'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

apiurl = "http://snehashishlaskar090.pythonanywhere.com/"
# apiurl= 'http://127.0.0.1:8000/'
usrName = None
psword = None


def convertUserDataToJson(username):
    data = requests.get('{}sites?username={}'.format(apiurl, username)).json()

    return data


@app.route('/auth', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:

            usrname = request.form['username']
            psword = request.form['password']

            data = requests.get(apiurl).json()
            
            for i in data:
                print(usrname, psword)
                if i[0] == usrname and i[1] == psword:
                    session['username'] = usrname
                    return redirect('/home')
        
            return render_template('login.html', error=True)

        else:
            return redirect('/home')

    else:
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:


            return render_template('login.html')

        else:
            return redirect('/home')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session['username'] = None
    print(session['username'])
    return redirect('/auth')

@app.route('/delete', methods=['POST','GET'])
def delete():
    return render_template('delete_account.html', sess=True)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user == None and pw == None:
            username = request.form['username']
            usrName = username
            password = request.form['password']
            psword = password

            email = request.form['email']
            try:
                convertUserDataToJson(username)
                return render_template('signup.html', msg = "User Already Exists!")
            except:
                if len(password) < 8:
                    return render_template('signup.html', msg = "Please select a password more than 8 digits!")
                else:

                    token = str(token_urlsafe(16))
                    if os.path.exists(path+'tokens.json'):
                        with open(path+'tokens.json', 'w') as file:
                            json.dump([], file)

                    with open(path+'tokens.json') as file:
                        data = json.load(file)

                    data.append(token)

                    with open(path+'tokens.json', 'w') as file:
                        json.dump(data, file)

                    try:
                        msg = Message(
                            'Confirmation Email',
                            sender='snehashish.laskar@gmail.com',
                            recipients=[email]
                        ) 
                        msg.body = render_template('email.html', username = username, link = f'https://snehashish08036.pythonanywhere.com/confirm/{token}')
                        msg.html = render_template('email.html', username = username, link = f'http://snehashish08036.pythonanywhere.com/confirm/{token}')
                        mail.send(msg)
                        return render_template('confirm.html')
                    except Exception as ex:
                        return str(ex)

        else:
            return redirect('/home')

    else:
        user = None
        pw = None

        try:
            user = session['username']
        except:
            pass

        if user != None and pw != None:
            return redirect('/home')
        else:
            return render_template('signup.html', msg = "")       


# Snehashish Laskar
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'add' in request.form:
            name = request.form['addname']
            email = request.form['addemail']
            username =  request.form['addusername']
            password = request.form['addpass']

            query = requests.post('{}addsite?username={}&sitename={}&password={}&email={}&siteusrname={}'.format(
                apiurl,
                session['username'],
                name,
                password,
                email,
                username,
            ))
            return redirect('/home')
        
        elif 'del' in request.form:
            name = request.form['name']

            query = requests.delete('{}delsite?username={}&site={}'.format(
                apiurl,
                session['username'],
                name
            ))

            return redirect('/home')
    else:
        return render_template('home.html', sess = True, data = convertUserDataToJson(session['username']))


@app.route('/cookies', methods = ['GET', 'POST'])
def cook():
    return jsonify(session['username'])
    
@app.route('/', methods = ['GET', 'POST'])
def main():

    user = None
    pw = None

    try:
        user = session['username']
    except:
        pass

    if user != None:
        return render_template('index.html', sess = True)
    else:
        return render_template('index.html', sess = False)

@app.route('/deleteusersure', methods=["GET", "POST"])
def deleteUser():

    requests.delete(f"{apiurl}delete?username={session['username']}")
    return redirect('/logout')



@app.route('/confirm/<token>', methods=['GET'])
def confirm(token):

    with open(path+'tokens.json') as file:
        data = json.load(file)

    if token in data:
        query = requests.post('{}createuser?username={}&password={}'.format(
                apiurl,usrName, psword
            ))
        session['username'] = usrName
        return redirect('/home')
    else:
        return redirect('/signup')

@app.route('/email', methods=['GET'])
def email():
    try:
        msg = Message(
            'Your Son',
            sender='snehashish.laskar@gmail.com',
            recipients=['snehashish.laskar@sahyadrischool.org', 'snehashish.laskar@gmail.com']
        )

        msg.body = render_template('email.html', username = 'Snehashish', link = 'https://snehashish08036.pythonanywhere.com/')
        msg.html = render_template('email.html', username = 'Snehashish', link = 'https://snehashish08036.pythonanywhere.com/')
        mail.send(msg)
        return render_template('confirm.html')
    except Exception as ex:
        return str(ex)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)