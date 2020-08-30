import multiprocessing
import time

from src import progress_queue
from src.main.main import start_scraper_process
from src.web_app.flask_app import start_app_windows, start_app


def main():
    multiprocessing.Process(target=start_scraper_process).start()
    start_app_windows()
    # start()


if __name__ == "__main__":
    main()

