from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)


if __name__ == '__main__':
    print("ok")
else:
    print("no main found")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        usecase = request.form['usecase']
        if usecase == 'sentimentAnalysis':
            return render_template("sentimentAnalysis.html")
        elif usecase == 'CustomerAnalysis': 
            return render_template("CustomerAnalysis.html")
@app.route("/heartbeat", methods=["GET", "POST"])
def heartbeat():
    return "200 OK";

@app.route("/sentimentAnalysis", methods=["GET", "POST"])
def sentimentAnalysis():
    df = pd.read_csv('C:\\Users\\gaura\\Downloads\\Dataset\\olist_reviews.csv')
    df["Sentiment"] = df["review_score"].apply(
        lambda rating: "Positive" if rating > 3 else "Negative"
    )
    df.loc[df.review_score == 3, 'Sentiment'] = "Neutral"
    df.groupby(['product_cat', 'Sentiment']).sum()

    response = {}
    if request.method == "POST":
        productName = request.form["productName"]
        filteredDf = df[df['product_cat'] == productName]
        response = filteredDf.groupby(['Sentiment']).sum().to_dict()
        response['productName'] = productName

    return render_template("sentimentAnalysis.html", response=response)

if __name__ == '__main__':
    print("ok")
    app.run()
else:
    print("no main found")            