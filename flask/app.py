# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', \
		title = 'Form Sample(get)', \
		message = '名前を入力して下さい。')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
	name = request.form['name']
	return render_template('index.html', \
		title = 'Form Sample(post)', \
		message = 'こんにちは、{}さん'.format(name))

if __name__ == '__main__':
	app.run()