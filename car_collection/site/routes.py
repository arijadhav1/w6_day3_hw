from flask import Blueprint, render_template

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/')
def home():
    print('This is the car page.')
    return render_template('index.html')