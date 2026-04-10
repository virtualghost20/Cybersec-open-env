from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Cybersec OpenEnv Server v0.1 - HF Space'})

@app.route('/reset', methods=['POST'])
def reset():
    return jsonify({'status': 'reset', 'obs': 'fastest'})

@app.route('/step', methods=['POST'])
def step():
    try:
        body = request.get_json() or {}
    except:
        body = {}
    return jsonify({'observation': {'result': 'fast'}, 'reward': 0.1, 'done': False, 'info': {'native': True}})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860, debug=False)

