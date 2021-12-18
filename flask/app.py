# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

# getのときの処理
@app.route('/', methods=['GET'])
def get():
	return render_template('index.html', \
		title = 'ボウリングのデータシート（ラウンドワン）', \
		message = '選べ')

# postのときの処理	
@app.route('/', methods=['POST'])
def post():
	name = request.form.getlist('progCB')
	return render_template('index.html', \
		title = 'ボウリングのデータシート（ラウンドワン）', \
		message = '{}をやれ'.format('と'.join(name)))

if __name__ == '__main__':
	app.run()