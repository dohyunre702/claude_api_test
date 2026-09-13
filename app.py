from flask import Flask, jsonify, render_template, request

from kakao_local_search import search_keyword

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    query = request.args.get("query", "").strip()
    if not query:
        return jsonify({"error": "검색어를 입력해주세요."}), 400

    try:
        data = search_keyword(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(data.get("documents", []))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
