from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# Load your vectorizer and model
vector = pickle.load(open("vectorizer.pkl", 'rb'))
model = pickle.load(open("phishing.pkl", 'rb'))

@app.route("/", methods=['GET', 'POST'])
def index():
    predict = None  # Default value
    
    if request.method == "POST":
        url = request.form['url']

        cleaned_url = re.sub(r'^(https?://)?(www\.)?', '', url)

       
        result = model.predict(vector.transform([cleaned_url]))[0]  # get first element
        
       
        if result == 'bad':
            predict = "🚨 This is a Phishing Website!!"
        elif result == 'good':
            predict = "✅ This is a Safe and Legitimate Website!"
        else:
            predict = "⚠️ Something went wrong!!"
    
   
    return render_template("index.html", predict=predict)


if __name__ == '__main__':
    app.run(debug=True)
