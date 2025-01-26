from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Shared data storage
data_store = []
executor = ThreadPoolExecutor()


# Endpoint: POST /data
@app.route("/data", methods=["POST"])
def add_data():
    global data_store
    input_data = request.json.get("data", [])
    if not isinstance(input_data, list) or not all(
        isinstance(i, int) for i in input_data
    ):
        return jsonify({"error": "Invalid input, provide a list of integers."}), 400
    data_store = input_data
    return jsonify({"message": "Data stored successfully"}), 200


# Concurrent task for sorting
def sort_data():
    return sorted(data_store)


# Concurrent task for finding top-n numbers
def find_top_n(n):
    return sorted(data_store, reverse=True)[:n]


# Concurrent task for calculating mean
def calculate_mean():
    return sum(data_store) / len(data_store) if data_store else 0


# Endpoint: GET /process/sort
@app.route("/process/sort", methods=["GET"])
def get_sorted_data():
    future = executor.submit(sort_data)
    sorted_data = future.result()
    return jsonify({"sorted_data": sorted_data}), 200


# Endpoint: GET /process/top-n
@app.route("/process/top-n", methods=["GET"])
def get_top_n():
    try:
        n = int(request.args.get("n", 0))
        if n <= 0 or n > len(data_store):
            raise ValueError
    except ValueError:
        return jsonify({"error": "Invalid value for n"}), 400
    future = executor.submit(find_top_n, n)
    top_n = future.result()
    return jsonify({"top_n": top_n}), 200


# Endpoint: GET /process/mean
@app.route("/process/mean", methods=["GET"])
def get_mean():
    future = executor.submit(calculate_mean)
    mean = future.result()
    return jsonify({"mean": mean}), 200


if __name__ == "__main__":
    app.run(debug=True)
