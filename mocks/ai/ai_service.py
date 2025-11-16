from flask import Flask, request, jsonify

app = Flask(__name__)

# --- تعريف الردود الخاصة ---
special_responses = {
    "/generate": "[Special mocked response] You hit the special endpoint!"
}

# --- الرد العام ---
general_response_template = "[General mocked response] You said: {}"

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "")

        # --- تحقق من special endpoint ---
        if request.path in special_responses:
            return jsonify({"response": special_responses[request.path]})

        # --- وإلا استخدم الرد العام ---
        return jsonify({"response": general_response_template.format(prompt)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/<path:any_path>", methods=["POST"])
def catch_all(any_path):
    try:
        data = request.get_json(force=True)
        prompt = data.get("prompt", "")
        return jsonify({"response": general_response_template.format(prompt)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9003)
