from flask import Flask, jsonify, render_template
import json, os
app = Flask(__name__)
BASE = os.path.expanduser("~/Cybertwin")
@app.route('/')
def dashboard():
    return render_template('index.html')
@app.route('/api/assets')
def assets():
    try:
        with open(f"{BASE}/scanner/scan_results.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify({"hosts":[]})
@app.route('/api/alerts')
def alerts():
    try:
        with open(f"{BASE}/monitoring/alerts.json") as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])
@app.route('/api/analysis')
def analysis():
    try:
        with open('/home/subhikshah/Cybertwin/sentinelrag/analysis.json') as f:
            return jsonify(json.load(f))
    except:
        return jsonify([])
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
