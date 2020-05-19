import slack
from src import config
from src.main.html_scraper import Scraper


client = slack.WebClient(token=config['bot_token'])
scraper = Scraper(link=config['fer_url'], payload={'username': config['username'], 'password': config['password']})

# locally
del config
