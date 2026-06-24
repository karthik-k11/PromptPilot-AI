from flask import Flask, render_template, request, jsonify, redirect, url_for

from prompt_optimizer import optimize_prompt
from prompt_scorer import analyze_prompt
from db import (
    create_database,
    save_prompt,
    get_prompt_history,
    delete_history
)

app = Flask(__name__)
create_database()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/history")
def history():

    history_data = get_prompt_history()

    return render_template(

        "history.html",

        history=history_data

    )

@app.route("/delete-history", methods=["POST"])
def clear_history():

    delete_history()

    return redirect(url_for("history"))


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

        # Analyze original prompt
        original_analysis = analyze_prompt(user_prompt)

        # Optimize prompt
        optimized_prompt = optimize_prompt(
            user_prompt,
            platform,
            prompt_type
        )

        # Analyze optimized prompt
        optimized_analysis = analyze_prompt(optimized_prompt)

        improvement = (
            optimized_analysis["score"]
            - original_analysis["score"]
        )
        save_prompt(

            original_prompt=user_prompt,

            optimized_prompt=optimized_prompt,

            platform=platform,

            prompt_type=prompt_type,

            original_score=original_analysis["score"],

            optimized_score=optimized_analysis["score"],

            score_improvement=improvement

        )

        return jsonify(
            {
                "success": True,

                "optimized_prompt": optimized_prompt,

                "original_score": original_analysis["score"],
                "original_level": original_analysis["level"],

                "optimized_score": optimized_analysis["score"],
                "optimized_level": optimized_analysis["level"],

                "score_improvement": improvement,

                "improvements": original_analysis["improvements"]
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