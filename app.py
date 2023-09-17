from flask import Flask, render_template, request
import os
from sanbproject.pipeline.prediction_pipeline import PredictionPipeline

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def get_index_page():
    if request.method == ["GET"]:
        return render_template("index.html")
    else:
        option = request.form.get("option")

        if option == "train_model":
            os.system("python main.py")
            return render_template("home.html")
        elif option == "open_home_page":
            return render_template("home.html")
        else:
            return render_template("index.html")
        
@app.route("/predict", methods=["POST"])
def predict():
    raw_review_text = request.form.get("review")
    prediction_pipeline = PredictionPipeline()
    prediction = prediction_pipeline.perform_prediction(str(raw_review_text))
    result = None

    if prediction == 1:
        result = "Positive"
    elif prediction == 0:
        result = "Negative"
    else:
        result = "Unknown Result"

    return render_template("home.html", result = result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)