from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return '<h1>Home</h1>'

@main.route('/profile')
def profile():
    return '<h1>Profile: </h1>'

@main.route('/about-us')
def about_us():
    return '<h1>About Us</h1>'
