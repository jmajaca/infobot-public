import slack
from src import config
from src.main.logger import Logger
from src.main.constants import log_file
from src.main.html_scraper import Scraper


client = slack.WebClient(token=config['bot_token'])
logger = Logger(log_file)
scraper = Scraper(link=config['fer_url'], payload={'username': config['username'], 'password': config['password']})

# locally
del config
