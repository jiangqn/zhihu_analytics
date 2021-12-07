import os
import sys
from flask import Flask
from flask import escape, url_for, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

from src.create_wordcloud import create_wordcloud

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

@app.route('/test')
def test():
    return 'test'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question_id = int(request.form.get('question_id'))
        create_wordcloud(question_id)
        return redirect(url_for('index'))
    return render_template('index.html')