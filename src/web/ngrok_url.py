import json
import os


def get_public_url():
    os.system("curl  http://localhost:4040/api/tunnels > tunnels.json")
    with open('tunnels.json') as data_file:
        data_json = json.load(data_file)
    for element in data_json['tunnels']:
        if 'https' in element['public_url']:
            public_url = element['public_url']
            return public_url


# https://github.com/inconshreveable/ngrok/issues/57#issuecomment-42587785
# https://stackoverflow.com/questions/27162552/ngrok-running-in-background
if __name__ == "__main__":
    print(get_public_url())
