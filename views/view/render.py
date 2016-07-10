from flask import render_template

def index():
    return render_template('index.html')

def home():
    return render_template('home.html')

def heat_map():
    return render_template('heatmap.html')

def addcontact():
    return render_template('add_contact.html')

def safest_route():
    return render_template('safest_route.html')