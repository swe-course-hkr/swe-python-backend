from flask import Blueprint, request, jsonify
from app.database.wrapper import Database
from app.database.userWrapper import UserDatabase
from app.socket import socketio
from app.util import successResponse, errorResponse


from app.routes.forms import UserForm, DeviceForm
from flask import render_template, redirect, flash

testSuiteRouter = Blueprint('testsuite', __name__)

#main testsuite page
@testSuiteRouter.route('/')
def index(): 
    user = {"username": 'aap'}
    return render_template('index.html', title='Home',user=user)

#create new user
@testSuiteRouter.route('/test/user/new', methods=['GET', 'POST'])
def newUser():
    form = UserForm()
    if form.validate_on_submit():
        print("creating new user...")
        new_user = UserDatabase.create_user(username=form.username.data,email=form.email.data,password=form.password.data)
        
        return redirect('/')

    return render_template('user.html', title='Create new user',crudAction='New',form=form)

#create new device
@testSuiteRouter.route('/test/device/new', methods=['GET', 'POST'])
def newDevice():
    form = DeviceForm()
    if form.validate_on_submit():
        print("create new device...")
        new_device = Database.add_device(name=form.devicename.data,type=form.devicetype.data,description=form.description.data)

        return redirect('/')
        

    return render_template('device.html', title='Create new device',crudAction='New',form=form)

