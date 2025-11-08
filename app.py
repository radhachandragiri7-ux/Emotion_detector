from flask import Flask, render_template, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "emotion_secret_key"

# Simple emotion-to-emoji mapping
EMO_EMOJI = {
    "Happy": "😄",
    "Sad": "😢",
    "Angry": "😠",
    "Surprise": "😲",
    "Neutral": "😐"
}

# Function to predict emotion (dummy logic — replace with ML model if needed)
def predict_emotion(text):
    text = text.lower()
    if "happy" in text or "good" in text or "great" in text or "love" in text:
        return "Happy"
    elif "sad" in text or "upset" in text or "depressed" in text:
        return "Sad"
    elif "angry" in text or "mad" in text or "furious" in text:
        return "Angry"
    elif "surprised" in text or "wow" in text or "shocked" in text:
        return "Surprise"
    else:
        return "Neutral"

@app.route("/", methods=["GET", "POST"])
def index():
    predicted_emotion = None
    emoji = None
    text = None
    emotions = {
        "Happy": random.randint(10, 100),
        "Sad": random.randint(10, 100),
        "Angry": random.randint(10, 100),
        "Surprise": random.randint(10, 100),
        "Neutral": random.randint(10, 100)
    }

    if request.method == "POST":
        text = request.form["text"]
        predicted_emotion = predict_emotion(text)
        emoji = EMO_EMOJI[predicted_emotion]

        # History logic
        if "history" not in session:
            session["history"] = []

        # Save latest 5 emotions
        session["history"].insert(0, {"text": text, "emotion": predicted_emotion, "emoji": emoji})
        session["history"] = session["history"][:5]

    return render_template(
        "index.html",
        emotion=predicted_emotion,
        emoji=emoji,
        chart_labels=list(emotions.keys()),
        chart_values=list(emotions.values()),
        user_input=text,
        history=session.get("history", []),
        EMO_EMOJI=EMO_EMOJI
    )

# ✅ Clear history route
@app.route("/clear_history", methods=["POST"])
def clear_history():
    session["history"] = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
