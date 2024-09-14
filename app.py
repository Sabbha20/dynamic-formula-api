from flask import Flask, request, jsonify
import json
import re

app = Flask(__name__)

# fetch formula and data
def parse_payload(data):
    dataset = data.get('data', [])
    formulas = data.get('formulas', [])
    return dataset, formulas

@app.route('/api/execute-formula', methods=['POST'])
def execute_formula():
    try:
        data = request.json
        # Logic is here
        dataset, formulas = parse_payload(data)
        # print(f"dataset - {dataset}")
        # print(f"formulas - {formulas}")
        return jsonify({"results": {}, "status": "success", "message": "Not implemented yet"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)