class SlackCommandUtils:

    @staticmethod
    def read_data(request, text_tokens_length=None):
        data = {}
        for key in request.form.keys():
            data[key] = request.form[key]
        data['text'] = data['text'].strip()
        if text_tokens_length is None:
            return data, True
        elif len(data['text'].split()) != text_tokens_length:
            return data, False
        else:
            data['text'] = data['text'].split()
            return data, True
