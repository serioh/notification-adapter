from flask import Flask, jsonify, request  # import objects from the Flask model
from email_service import authenticate, send_message, create_message

app = Flask(__name__)  # define app using Flask


@app.route('/', methods=['POST'])
def read_html():
    html_message = request.data.decode("UTF-8")
    recipient = request.headers.get('recipient')
    subject = request.headers.get('subject')
    service = authenticate()
    send_message(service, 'me',
                 create_message('me', recipient, subject, html_message))
    return "hi"


if __name__ == '__main__':
    app.run(debug=True)  # run app on port 8080 in debug mode