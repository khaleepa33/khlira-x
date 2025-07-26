from flask import Flask, render_template, request, jsonify
import khlira_mt5
import json

app = Flask(__name__)

@app.route("/")
def home():
    with open("khlira_config.json") as f:
        config = json.load(f)
    return render_template("index.html", config=config)

@app.route("/trade", methods=["POST"])
def trade():
    action = request.json.get("action")
    try:
        khlira_mt5.connect()
        if action == "buy":
            result = khlira_mt5.place_buy()
        elif action == "sell":
            result = khlira_mt5.place_sell()
        else:
            return jsonify({"status": "error", "msg": "Invalid action"}), 400
        return jsonify({"status": "success", "result": result._asdict()})
    except Exception as e:
        return jsonify({"status": "error", "msg": str(e)}), 500

@app.route("/update-config", methods=["POST"])
def update_config():
    data = request.json
    with open("khlira_config.json", "w") as f:
        json.dump(data, f, indent=2)
    return jsonify({"status": "updated"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=50000,debug=True)
