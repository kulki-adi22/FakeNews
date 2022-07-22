from flask import Flask, render_template,request

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')
@app.route('/fakeNews')
def fakeNews():
    return render_template('fakeNews.html')
@app.route('/hateSpeech')
def hateSpeech():
    return render_template('hateSpeech.html')
@app.route('/fakeTest',methods=['GET','POST'])
def fakeTest():
    output =  request.form['news']
    print(output)
    return render_template('hateSpeech.html',op=output)
@app.route('/hateTest',methods=['GET','POST'])
def hateTest():
    output =  request.form['text']
    print(output)
    return output
if __name__ == '__main__':
    app.run(debug=True, port=5001)