from flask import Blueprint, request, jsonify
from app.database.wrapper import Database
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
        pass

    return render_template('user.html', title='Create new user',crudAction='New',form=form)

#create new device
@testSuiteRouter.route('/test/device/new', methods=['GET', 'POST'])
def newDevice():
    form = DeviceForm()
    if form.validate_on_submit():
        pass

    return render_template('device.html', title='Create new device',crudAction='New',form=form)

