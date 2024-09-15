from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_simple_addition():
    response = client.post(
        "/api/execute-formula",
        json={
            "data": [{"id": 1, "fieldA": 10}, {"id": 2, "fieldA": 20}],
            "formulas": [
                {
                    "outputVar": "result",
                    "expression": "fieldA + 10",
                    "inputs": [{"varName": "fieldA", "varType": "number"}],
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["results"] == {"result": [20, 30]}


def test_formula_chaining():
    response = client.post(
        "/api/execute-formula",
        json={
            "data": [
                {"id": 1, "fieldA": 10, "fieldB": 2},
                {"id": 2, "fieldA": 20, "fieldB": 3},
            ],
            "formulas": [
                {
                    "outputVar": "sumResult",
                    "expression": "fieldA + fieldB",
                    "inputs": [
                        {"varName": "fieldA", "varType": "number"},
                        {"varName": "fieldB", "varType": "number"},
                    ],
                },
                {
                    "outputVar": "finalResult",
                    "expression": "sumResult * 2 + fieldA",
                    "inputs": [
                        {"varName": "sumResult", "varType": "number"},
                        {"varName": "fieldA", "varType": "number"},
                    ],
                },
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["results"] == {
        "sumResult": [12, 23],
        "finalResult": [34, 66],
    }


def test_currency_and_percentage():
    response = client.post(
        "/api/execute-formula",
        json={
            "data": [
                {
                    "id": 1,
                    "product": "Laptop",
                    "unitPrice": "1000 USD",
                    "quantity": 5,
                    "discount": "10%",
                },
                {
                    "id": 2,
                    "product": "Smartphone",
                    "unitPrice": "500 USD",
                    "quantity": 10,
                    "discount": "5%",
                },
                {
                    "id": 3,
                    "product": "Tablet",
                    "unitPrice": "300 USD",
                    "quantity": 15,
                    "discount": "0%",
                },
            ],
            "formulas": [
                {
                    "outputVar": "revenue",
                    "expression": "((unitPrice * quantity) - (unitPrice * quantity * discount))",
                    "inputs": [
                        {"varName": "unitPrice", "varType": "currency"},
                        {"varName": "quantity", "varType": "number"},
                        {"varName": "discount", "varType": "percentage"},
                    ],
                }
            ],
        },
    )
    assert response.status_code == 200
    assert response.json()["results"] == {"revenue": [4500.00, 4750.00, 4500.00]}
