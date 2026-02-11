from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

# Load model and encoder
model = pickle.load(open("model/stress_model.pkl", "rb"))
encoder = pickle.load(open("model/label_encoder.pkl", "rb"))

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    advice = ""
    css_class = ""
    sleep = study = mood = 0

    if request.method == "POST":
        sleep = int(request.form["sleep"])
        study = int(request.form["study"])
        mood = int(request.form["mood"])

        prediction = model.predict([[sleep, study, mood]])
        result = encoder.inverse_transform(prediction)[0]

        # Simple advice logic
        if result == "Low":
            advice = "You're doing well! Maintain your healthy routine 😊"
            css_class = "low"
        elif result == "Medium":
            advice = "Try balancing study and rest better ⚖️"
            css_class = "medium"
        else:
            advice = "High stress detected! Take breaks and seek support ❤️"
            css_class = "high"

    return render_template(
        "index.html",
        result=result,
        advice=advice,
        css_class=css_class,
        sleep=sleep,
        study=study,
        mood=mood
    )

if __name__ == "__main__":
    app.run(debug=True)
