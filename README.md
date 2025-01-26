# Flask Concurrent API

A containerized Flask application with a RESTful API for processing numerical data. 
It supports sorting, finding the top N numbers, and calculating the mean with concurrent request handling.

## Features

* Endpoints:
  * POST /data: Store a list of integers.
  * GET /process/sort: Returns numbers in ascending order.
  * GET /process/top-n: Returns the top N largest numbers.
  * GET /process/mean: Returns the mean of the numbers.
* Concurrency: Handles multiple requests efficiently.
* Tests: Includes unit tests for all endpoints.

## Quick start

### Using Docker
1. Build and run:
```bash
docker compose up --build
```

2. Use the API
Use a tool like curl or Postman to send requests to the API.

Example:
```bash
curl -X POST http://localhost:5001/data \
     -H "Content-Type: application/json" \
     -d '{"data": [1, 2, 3, 4, 5]}'
```

Expected response:
```json
{
  "message": "Data stored successfully."
}
```

Now you can use the other endpoints to process the data.

3. Stop container:
```bash
docker compose down
```

### Run locally (without Docker)
1. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Use the API as described above.

## API Endpoints

| Endpoint            | Method | Description                     | Example Request                                                                                      |
|---------------------|--------|---------------------------------|------------------------------------------------------------------------------------------------------|
| `/data`             | POST   | Store integers for processing. | `curl -X POST -H "Content-Type: application/json" -d '{"data": [1,2,3]}' http://127.0.0.1:5001/data` |
| `/process/sort`     | GET    | Get sorted numbers.            | `curl http://127.0.0.1:5001/process/sort`                                                            |
| `/process/top-n?n=3`| GET    | Get top N largest numbers.     | `curl http://127.0.0.1:5001/process/top-n?n=3`                                                       |
| `/process/mean`     | GET    | Get mean of numbers.           | `curl http://127.0.0.1:5001/process/mean`                                                            |

## Tests

Run the tests with docker:
```bash
docker-compose run flask pytest
```

Run the tests locally:
```bash
pytest
```
