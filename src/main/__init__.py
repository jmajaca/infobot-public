import slack
from src import config
from src.main.objects.web_scraper import WebScraper


client = slack.WebClient(token=config['bot_token'])
scraper = WebScraper(link=config['fer_url'], payload={'username': config['username'], 'password': config['password']})

# locally
del config
