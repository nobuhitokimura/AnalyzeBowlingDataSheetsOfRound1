from flask import Flask, render_template

# Flaskクラスのインスタンス生成
app = Flask(__name__)

@app.route('/') # URLを指定。URLにリクエストが来ると関数が実行される
def index():
    title = 'world'
    framework = 'Flask'
    mark = '!'
    return render_template('index.html', title=title, framework=framework, mark=mark)

if __name__ == '__main__':
    app.run()
