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

