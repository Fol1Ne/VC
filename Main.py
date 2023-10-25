from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from project.Forms import LoginForm, RegisterForm, EditForm, SetPasswordForm, SetEmailForm, DeletePageForm, SetImageForm, AddImageForm, AddNewPost
from config import Config
from werkzeug.utils import secure_filename
import pickle
import os
import datetime

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config.from_object(Config)

if os.path.exists('Users'):
    Users = open('Users', 'rb')
    users = pickle.load(Users)
    Users.close()
else:
    Users = open('Users', 'wb')
    pickle.dump([], Users)
    users = []
    Users.close()

currentUser = False

@app.route("/", methods=["get", "post"])
def Login():
    global currentUser
    currentUser = False
    form = LoginForm()
    if form.validate_on_submit():
        login = form.login.data
        password = form.password.data
        for i in users:
            if i['login'] == login and i['password'] == password:
                currentUser = i
                return redirect(url_for("MyPage"))

    return render_template("Login.html", form=form)

@app.route("/Home", methods=["get", "post"])
def MyPage():
    global currentUser
    global users
    form = AddNewPost()
    if form.validate_on_submit():
        text = form.text.data
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'photos', filename))
        photo = '/static/photos/' + filename
        date = datetime.datetime.today().strftime("%d/%m/%Y")
        post = [text, photo, date]
        posts = []
        posts.append(post)

        for i in currentUser['Posts']:
            posts.append(i)

        for i in range(len(users)):
            if users[i]['login'] == currentUser['login']:
                users[i]['Posts'] = posts
                currentUser = users[i]
        Users = open('Users', 'wb')
        pickle.dump(users, Users)
        Users.close()
        return redirect(url_for("MyPage"))
    return render_template("MyPage.html", form=form, currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], currentUserNativeCity=currentUser['nativeCity'], currentUserAvatar=currentUser['avatarImage'], currentUserPhotos=currentUser['Photos'], currentUserPosts=currentUser['Posts'])

@app.route("/Register", methods=["get", "post"])
def Register():
    form = RegisterForm()
    if form.validate_on_submit():
        next = True
        login = form.login.data
        password = form.password.data
        name = form.name.data
        surname = form.surname.data
        email = form.email.data
        nativeCity = form.nativeCity.data
        avatarImage = '/static/photos/noName.png'
        Photos = []
        Posts = []
        for i in users:
            if i['login'] == login:
                next = False
                break
        if next == True:
            user = {'login': login, 'password': password, 'name': name, 'surname': surname, 'email': email, 'nativeCity': nativeCity, 'avatarImage': avatarImage, 'Photos': Photos, 'Posts': Posts}
            users.append(user)
            Users = open('Users', 'wb')
            pickle.dump(users, Users)
            Users.close()
            return redirect(url_for("Login"))

    return render_template("Register.html", form=form)

@app.route("/Message")
def Message():
    return render_template("Message.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/Friends")
def Friends():
    return render_template("Friends.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/Community")
def Community():
    return render_template("Community.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/News")
def News():
    return render_template("News.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/Photo")
def Photo():
    return render_template("Photo.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/Edit", methods=["get", "post"])
def Edit():
    global currentUser
    global users
    form = EditForm()
    form.name.data = currentUser['name']
    form.surname.data = currentUser['surname']
    form.nativeCity.data = currentUser['nativeCity']
    newName = form.name.data
    newSurname = form.surname.data
    newNativeCity = form.nativeCity.data
    newUsers = []
    if form.validate_on_submit():
        for i in users:
            if i['login'] == currentUser['login']:
                login = currentUser['login']
                password = currentUser['password']
                email = currentUser['email']
                if newName.split() == '':
                    newName = currentUser['name']
                if newSurname.split() == '':
                    newSurname = currentUser['surname']
                if newNativeCity.split() == '':
                    newNativeCity = currentUser['nativeCity']
                user = {'login': login, 'password': password, 'name': newName, 'surname': newSurname, 'email': email, 'nativeCity': newNativeCity, 'avatarImage': currentUser['avatarImage'], 'Photos': currentUser['Photos'], 'Posts': currentUser['Posts']}
                newUsers.append(user)
                currentUser = user
            else:
                newUsers.append(i)
        Users = open('Users', 'wb')
        pickle.dump(newUsers, Users)
        Users.close()
        users = newUsers
        print(newUsers)
        return redirect(url_for("Edit"))
    return render_template("Edit.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/Settings", methods=["get", "post"])
def Settings():
    return render_template("Settings.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'])

@app.route("/SetPassword", methods=["get", "post"])
def SetPassword():
    global currentUser
    global users
    form = SetPasswordForm()
    if form.validate_on_submit():
        oldPassword = form.oldPassword.data
        newPassword = form.newPassword.data
        newUsers = []
        for i in users:
            if i['login'] == currentUser['login'] and i['password'] == oldPassword:
                login = currentUser['login']
                password = newPassword
                name = i['name']
                surname = i['surname']
                email = i['email']
                nativeCity = i['nativeCity']
                user = {'login': login, 'password': password, 'name': name, 'surname': surname, 'email': email, 'nativeCity': nativeCity, 'avatarImage': currentUser['avatarImage'], 'Photos': currentUser['Photos'], 'Posts': currentUser['Posts']}
                newUsers.append(user)
                currentUser = user
            else:
                newUsers.append(i)
        Users = open('Users', 'wb')
        pickle.dump(newUsers, Users)
        Users.close()
        users = newUsers
        print(newUsers)
        return redirect(url_for("SetPassword"))

    return render_template("SetPassword.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/SetEmail", methods=["get", "post"])
def SetEmail():
    global currentUser
    form = SetEmailForm()
    if form.validate_on_submit():
        newEmail = form.newEmail.data
        password = form.password.data
        for i in range(len(users)):
            if users[i]['login'] == currentUser['login'] and users[i]['password'] == password:
                users[i]['email'] = newEmail
                currentUser = users[i]
        Users = open('Users', 'wb')
        pickle.dump(users, Users)
        Users.close()
        print(users)
        return redirect(url_for("SetEmail"))
    return render_template("SetEmail.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/DeletePage", methods=["get", "post"])
def DeletePage():
    global currentUser
    form = DeletePageForm()
    if form.validate_on_submit():
        password = form.password.data
        for i in range(len(users)):
            if users[i]['login'] == currentUser['login'] and users[i]['password'] == password:
                del users[i]
                currentUser = False
                Users = open('Users', 'wb')
                pickle.dump(users, Users)
                Users.close()
                print(users)
                return redirect(url_for("Login"))

    return render_template("DeletePage.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/SetImage", methods=["get", "post"])
def SetImage():
    global currentUser
    form = SetImageForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'photos', filename))
        userAvatar = '/static/photos/' + filename
        for i in range(len(users)):
            if users[i]['login'] == currentUser['login']:
                users[i]['avatarImage'] = userAvatar
                currentUser = users[i]
        Users = open('Users', 'wb')
        pickle.dump(users, Users)
        Users.close()
        return redirect(url_for("MyPage"))

    return render_template("SetImage.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/AddImage", methods=["get", "post"])
def AddImage():
    global currentUser
    form = AddImageForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'photos', filename))
        Photo = '/static/photos/' + filename
        Photos = []
        Photos.append(Photo)

        for i in currentUser['Photos']:
            Photos.append(i)

        for i in range(len(users)):
            if users[i]['login'] == currentUser['login']:
                users[i]['Photos'] = Photos
                currentUser = users[i]
        Users = open('Users', 'wb')
        pickle.dump(users, Users)
        Users.close()
        return redirect(url_for("MyPage"))

    return render_template("AddImage.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], form=form)

@app.route("/ViewImage", methods=["get", "post"])
def ViewImage():
    global currentUser
    return render_template("ViewImage.html", currentUserName=currentUser['name'], currentUserSurname=currentUser['surname'], currentUserPhotos=currentUser['Photos'])
if __name__ == '__main__':
    app.run(host='localhost', port='5000')