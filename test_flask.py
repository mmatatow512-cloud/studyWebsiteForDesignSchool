from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/test', methods=['POST'])
def test_post():
    return {'message': 'Test POST successful'}

if __name__ == '__main__':
    app.run(debug=True, port=5002)
