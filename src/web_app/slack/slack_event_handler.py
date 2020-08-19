from src.web_app.flask_app import app
from flask import request, Response
from src.main import client
from src.main.reactions import count_reactions, generate_reactions_message
import re
import multiprocessing


@app.route('/slack/', methods=['POST'])
def slack_event_handler():
    # return Response(request.json['challenge']), 200
    data = request.json
    message = str(data['event']['text'])
    if re.search(r'^<@[A-Z0-9]+> *count *$', message):
        # TODO slack client timeout
        multiprocessing.Process(target=count_reactions, args=(client,)).start()
        return Response(), 200
    elif re.search(r'^<@[A-Z0-9]+> *:(.*): *$', message):
        answer_msg = generate_reactions_message(re.search(':(.*):', data['event']['text']).group(1))
        response = client.chat_postMessage(channel=data['event']['channel'], text=answer_msg)
        return Response(), 200
    return Response(), 404
