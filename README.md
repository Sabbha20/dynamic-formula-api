# Dynamic Formula API

This API allows for dynamic processing and analysis of complex datasets using user-defined formulas.

## Setup and Deployment Instructions

1. Ensure you have Python 3.12+ installed on your system.

2. Clone this repository:
```
git clone git@github.com:Sabbha20/dynamic-formula-api.git
cd dynamic-formula-api
```
3. Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate 
```
> On Windows, use `venv\Scripts\activate`

4. Install the required packages:
```
pip install -r requirements.txt
```
5. Run the API:
```
uvicorn main:app --reload
```
6. The API will be available at
`http://localhost:8000`. You can access the 
interactive API documentation at `http://localhost:8000/docs`.

## API Usage

Send a POST request to `/api/execute-formula` with a JSON payload containing your dataset and formulas. Refer to the API documentation for detailed request and response formats.

## Testing
To run the test cases, run:
```
pytest test_main.py
```

## Performance Considerations

- The API uses efficient algorithms for formula parsing and execution.
- Decimal is used for precise arithmetic calculations.
- Formula dependencies are resolved to determine the optimal execution order.

## Design Patterns

- Factory Pattern: Used in the `safe_eval` function to create a safe execution environment.
- Strategy Pattern: Different strategies are used for preprocessing different data types.
- Chain of Responsibility: Formula execution follows a chain based on dependencies.

## Coding Standards

- PEP 8 guidelines are followed for code style.
- Type hints are used for better code readability and IDE support.
- Error handling is implemented using FastAPI's built-in exception handling.

# Sample Input:
```
{
  "data": [
    {
      "id": 1,
      "product": "Laptop",
      "unitPrice": "1000 USD",
      "quantity": 5,
      "discount": "10%"
    },
    {
      "id": 2,
      "product": "Smartphone",
      "unitPrice": "500 USD",
      "quantity": 10,
      "discount": "5%"
    },
    {
      "id": 3,
      "product": "Tablet",
      "unitPrice": "300 USD",
      "quantity": 15,
      "discount": "0%"
    }
  ],
  "formulas": [
    {
      "outputVar": "revenue",
      "expression": "((unitPrice * quantity) - (unitPrice * quantity * discount))",
      "inputs": [
        {
          "varName": "unitPrice",
          "varType": "currency"
        },
        {
          "varName": "quantity",
          "varType": "number"
        },
        {
          "varName": "discount",
          "varType": "percentage"
        }
      ]
    }
  ]
}
```

# Sample Output:
```
{
  "results": {
    "revenue": [
      4500,
      4750,
      4500
    ]
  },
  "status": "success",
  "message": "The formulas were executed successfully."
}
```