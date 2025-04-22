from flask import Flask, request, jsonify

app = Flask(__name__)
nodes = []  # 登録されたノードを保持するリスト

# 🔹 ノード登録エンドポイント
@app.route("/register_node", methods=["POST"])
def register_node():
    data = request.get_json()
    print("📥 ノード登録:", data)

    # 重複登録防止（IPとポートが同じなら上書き）
    global nodes
    nodes = [n for n in nodes if not (n["ip"] == data["ip"] and n["port"] == data["port"])]
    nodes.append(data)

    return jsonify({"status": "registered"}), 200

@app.route("/get_nodes",methods=["GET"])
def get_best_nodes():
    sorted_data = sorted(
        nodes,
        key=lambda n: (
            n.get("cpu", 100),
            n.get("memory", 100),
            n.get("gpu", 100 if n.get("gpu", -1) == -1 else n["gpu"])
        )
    )
    return sorted_data



# 🔹 最適ノード取得エンドポイント
@app.route("/get_best_node", methods=["GET"])
def get_best_node():
    model = request.args.get("model")
    if not model:
        return jsonify({"error": "モデル名が指定されていません"}), 400

    # モデル名でフィルタ
    candidates = [n for n in nodes if n["model"] == model]
    if not candidates:
        return jsonify({"error": f"利用可能なノードが見つかりません: {model}"}), 404

    # 使用率が低い順にソート（GPUが未定義なら重く評価）
    best = sorted(
        candidates,
        key=lambda n: (
            n.get("cpu", 100),
            n.get("memory", 100),
            n.get("gpu", 100 if n.get("gpu", -1) == -1 else n["gpu"])
        )
    )[0]

    return jsonify({
        "ip": best["ip"],
        "port": best["port"],
        "model": best["model"]
    }), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
