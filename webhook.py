from flask import Flask,request,json

app = Flask(__name__)

@app.route('/',methods=['POST'])
def githubIssue():
    if request.method == 'POST'and request.content_length > 0 :
        print("Data received from Webhook is: ", request.json['title'])
        return "Webhook received!"

#Todo: Webhook -> api -> db Todo
#Todo: Webhook -> api -> check all (if down)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')