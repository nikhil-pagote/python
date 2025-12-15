from flask import Flask

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "<h1>Hello, World!</h1>"


# Variable Rule
# @app.route('/success/<score>')
@app.route("/success/<int:score>", methods=["GET"])
def success(score):
    # return f'Person is passed and scrore is: {score}'
    return f"Person is passed and scrore is: {str(score)}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
