from flask import Flask, request, jsonify
import json
import re
from datetime import datetime
import math
from decimal import Decimal, getcontext

getcontext().prec = 10


app = Flask(__name__)

def safe_eval(expr, variables):
    safe_dict = {
        'abs': abs, 'round': round, 'min': min, 'max': max,
        'sum': sum, 'pow': pow, 'math': math, 'Decimal': Decimal
    }
    safe_dict.update(variables)
    return eval(expr, {"__builtins__": None}, safe_dict)

def execute_formula(formula, row):
    try:
        result = safe_eval(formula['expression'], row)
        print(f"result - {round(result, 2)}")
        return round(result, 2)
    except Exception as e:
        return f"Error: {str(e)}"

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
                if re.match(r'^[\$£€]?[\d,]+(\.\d{2})?(\s?[A-Z]{3})?$', value):
                    row[key] = Decimal(re.sub(r'[^\d.]', '', value))
                # Handle percentage
                elif value.endswith('%'):
                    row[key] = Decimal(value.rstrip('%')) / 100
                # Handle date
                elif re.match(r'^\d{4}-\d{2}-\d{2}$', value):
                    row[key] = datetime.strptime(value, '%Y-%m-%d')
            elif isinstance(value, (int, float)):
                row[key] = Decimal(str(value))
    return dataset

# validating inputs
def validate_formula(formula, dataset, created_vars):
    expression = formula['expression']
    inputs = formula['inputs']
    
    print(f"expression - {expression}")
    print(f"inputs - {inputs}")
    
    # Check if all input variables are present in the dataset or created_vars
    for input_var in inputs:
        if input_var['varName'] not in dataset[0] and input_var['varName'] not in created_vars:
            return False, f"Input variable {input_var['varName']} not found in dataset or previous formulas"
    
    # Basic syntax check (this can be expanded)
    if not re.match(r'^[a-zA-Z0-9\s\+\-\*\/\(\)]+$', expression):
        return False, "Invalid characters in expression"
    
    return True, "Formula is valid"


MAX_ITERATIONS = 1000

def execute_formulas(dataset, formulas):
    results = {}
    execution_order = determine_execution_order(formulas)
    
    for row in dataset:
        iterations = 0
        for output_var in execution_order:
            formula = next(f for f in formulas if f['outputVar'] == output_var)
            row[output_var] = execute_formula(formula, row)
            iterations += 1
            if iterations > MAX_ITERATIONS:
                raise ValueError("Execution exceeded maximum allowed iterations")
        
        for output_var in execution_order:
            if output_var not in results:
                results[output_var] = []
            results[output_var].append(row[output_var])
    
    return results

def determine_execution_order(formulas):
    dependencies = {f['outputVar']: set() for f in formulas}
    for formula in formulas:
        for input_var in formula['inputs']:
            if input_var['varName'] in dependencies:
                dependencies[formula['outputVar']].add(input_var['varName'])
    
    execution_order = []
    while dependencies:
        # Find all nodes with no dependencies
        ready = [node for node, deps in dependencies.items() if not deps]
        if not ready:
            raise ValueError("Circular dependency detected")
        execution_order.extend(ready)
        # Remove the ready nodes and update dependencies
        for node in ready:
            del dependencies[node]
            for deps in dependencies.values():
                deps.discard(node)
    
    return execution_order

@app.route('/api/execute-formula', methods=['POST'])
def execute_input_data():
    try:
        data = request.json
        # Logic is here
        dataset, formulas = parse_payload(data)
        dataset = preprocess_data(dataset)
        print(f"dataset - {dataset}")
        print(f"formulas - {formulas}")
        
        
        # remove previous entry
        created_vars = set()
        for formula in formulas:
            is_valid, message = validate_formula(formula, dataset, created_vars)
            if not is_valid:
                return jsonify({"status": "error", "message": message}), 400
            created_vars.add(formula['outputVar'])
        
        
        results = execute_formulas(dataset, formulas)
        return jsonify({
            "results": results,
            "status": "success",
            "message": "The formulas were executed successfully."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)