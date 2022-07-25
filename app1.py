from flask import Flask, render_template,request
import pickle
from numpy import vectorize
import pandas 
import re
import string

from sklearn.model_selection import train_test_split
app = Flask(__name__)
from sklearn.feature_extraction.text import TfidfVectorizer
tfvect = TfidfVectorizer()
df_fake = pandas.read_csv("Fake.csv")
df_true = pandas.read_csv("True.csv")
df_fake["class"] = 0
df_true["class"] = 1
vectorization = TfidfVectorizer()
df_merge = pandas.concat([df_fake, df_true], axis =0 )
df_merge.columns
df = df_merge.drop(["title", "subject","date"], axis = 1)
df = df.sample(frac = 1)
df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text
df["text"] = df["text"].apply(wordopt)
x = df["text"]
y = df["class"]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25)
tfid_x_train = tfvect.fit_transform(x_train)
tfid_x_test = tfvect.transform(x_test)
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
    # print(output)
    # return render_template('hateSpeech.html',op=output)
    loaded_model = pickle.load(open('model (2).pkl','rb'))
    input_data = [output]
    vectorized_data = tfvect.transform(input_data)
    prediction = loaded_model.predict(vectorized_data)
    return prediction

@app.route('/hateTest',methods=['GET','POST'])
def hateTest():
    output =  request.form['text']
    print(output)
    return output
if __name__ == '__main__':
    app.run(debug=True, port=5001)
