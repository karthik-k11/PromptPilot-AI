from flask import Flask, render_template, request, jsonify

from prompt_optimizer import optimize_prompt
from prompt_scorer import analyze_prompt

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/optimize", methods=["POST"])
def optimize():

    try:

        data = request.get_json()

        user_prompt = data.get("prompt", "").strip()
        platform = data.get("platform", "")
        prompt_type = data.get("prompt_type", "")

        if not user_prompt:

            return jsonify(
                {
                    "success": False,
                    "message": "Please enter a prompt."
                }
            ), 400

        # Analyze the original prompt
        analysis = analyze_prompt(user_prompt)

        # Optimize the prompt using Gemini
        optimized_prompt = optimize_prompt(
            user_prompt,
            platform,
            prompt_type
        )

        return jsonify(
            {
                "success": True,
                "optimized_prompt": optimized_prompt,
                "score": analysis["score"],
                "level": analysis["level"],
                "improvements": analysis["improvements"]
            }
        )

    except Exception as e:

        return jsonify(
            {
                "success": False,
                "message": str(e)
            }
        ), 500


if __name__ == "__main__":
    app.run(debug=True)