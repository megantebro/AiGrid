from flask import Flask, request, jsonify

app = Flask(__name__)
nodes = {}  # node_id: {"cpu": ..., "memory": ..., "last_seen": ...}

@app.route("/report", methods=["POST"])
def report():
    data = request.json
    node_id = data["node_id"]
    nodes[node_id] = {
        "cpu": data["cpu"],
        "memory": data["memory"],
        "last_seen": time.time()
    }
    return jsonify({"status": "ok"})

@app.route("/get_best_node", methods=["GET"])
def get_best_node():
    sorted_nodes = sorted(nodes.items(), key=lambda x: (x[1]["cpu"], -x[1]["memory"]))
    if sorted_nodes:
        return jsonify({"best_node": sorted_nodes[0][0]})
    return jsonify({"error": "no available nodes"}), 404

if __name__ == "__main__":
    import time
    app.run(debug=True)