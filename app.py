from flask import Flask, request, jsonify
import json
import re
from datetime import datetime
import math
from decimal import Decimal

app = Flask(__name__)

# fetch formula and data
def parse_payload(data):
    dataset = data.get('data', [])
    formulas = data.get('formulas', [])
    return dataset, formulas

# preprocessing data
def preprocess_data(dataset):
    for row in dataset:
        for key, value in row.items():
            if isinstance(value, str):
                # Handle currency
                if re.match(r'^\$?[\d,]+(\.\d{2})?$', value):
                    row[key] = Decimal(re.sub(r'[^\d.]', '', value))
                # Handle percentage
                elif value.endswith('%'):
                    row[key] = Decimal(value.rstrip('%')) / 100
                # Handle date
                elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
    return dataset

@app.route('/api/execute-formula', methods=['POST'])
def execute_formula():
    try:
        data = request.json
        # Logic is here
        dataset, formulas = parse_payload(data)
        dataset = preprocess_data(dataset)
        print(f"dataset - {dataset}")
        print(f"formulas - {formulas}")
        return jsonify({"results": {}, "status": "success", "message": "Not implemented yet"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)