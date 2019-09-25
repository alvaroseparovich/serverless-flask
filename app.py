from flask import Flask, render_template, request
import json

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])
def main():
    
    data = json.loads(request.get_data())
    print("Id processed:  ----- " + str(data['id']))
    return ""


if __name__ == "__main__":
    app.run()
