import re
from decimal import Decimal, getcontext, InvalidOperation
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union
import logging

app = FastAPI(title="Dynamic Formula Execution API")
getcontext().prec = 10

logging.basicConfig(level=logging.DEBUG)


class InputVariable(BaseModel):
    varName: str
    varType: str


class Formula(BaseModel):
    outputVar: str
    expression: str
    inputs: List[InputVariable]


class APIRequest(BaseModel):
    data: List[Dict[str, Union[str, int, float]]]
    formulas: List[Formula]


def preprocess_data(dataset):
    for row in dataset:
        for key, value in row.items():
            if isinstance(value, str):
                if re.match(r"^[\$£€]?[\d,]+(\.\d{2})?(\s?[A-Z]{3})?$", value):
                    # Handle currency
                    row[key] = Decimal(re.sub(r"[^\d.]", "", value))
                elif value.endswith("%"):
                    # Handle percentage
                    row[key] = Decimal(value.rstrip("%")) / Decimal("100")
                else:
                    # Keep other strings as they are
                    pass
            elif isinstance(value, (int, float)):
                row[key] = Decimal(str(value))
        logging.debug(f"Preprocessed row: {row}")
    return dataset


def safe_eval(expr, variables):
    safe_dict = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "Decimal": Decimal,
    }
    for key, value in variables.items():
        if isinstance(value, Decimal):
            safe_dict[key] = value
        else:
            try:
                safe_dict[key] = Decimal(str(value))
            except InvalidOperation:
                safe_dict[key] = value

    logging.debug(f"Evaluating expression: {expr}")
    logging.debug(f"Variables: {safe_dict}")

    try:
        result = eval(expr, {"__builtins__": None}, safe_dict)
        logging.debug(f"Evaluation result: {result}")
        return result
    except Exception as e:
        logging.error(f"Error evaluating expression '{expr}': {str(e)}")
        raise


def execute_single_formula(formula, row):
    try:
        result = safe_eval(formula.expression, row)
        return round(result, 2)
    except Exception as e:
        logging.error(
            f"Error in formula execution for '{formula.expression}': {str(e)}"
        )
        raise HTTPException(
            status_code=400,
            detail=f"Error in formula execution for '{formula.expression}': {str(e)}",
        )


@app.post("/api/execute-formula")
async def execute_formula(request: APIRequest):
    dataset = preprocess_data(request.data)
    results = {}

    for row in dataset:
        for formula in request.formulas:
            row[formula.outputVar] = execute_single_formula(formula, row)

        for formula in request.formulas:
            if formula.outputVar not in results:
                results[formula.outputVar] = []
            results[formula.outputVar].append(row[formula.outputVar])

    return {
        "results": results,
        "status": "success",
        "message": "The formulas were executed successfully.",
    }
