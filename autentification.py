from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data['username'] == 'admin' and data['password'] == '1234':
        return jsonify(token="jwt_token")
    return jsonify(error="Unauthorized"), 401

if __name__ == '__main__':
    app.run(port=5001)
