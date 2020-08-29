import multiprocessing

from src import progress_queue
from src.main.main import start
from src.web_app.flask_app import start_app_windows


def main():
    multiprocessing.Process(target=start).start()
    start_app_windows()
    # start()


if __name__ == "__main__":
    main()

