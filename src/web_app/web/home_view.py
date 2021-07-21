import multiprocessing

from src.main.main import start_scraper_process
from src import logger, progress_queue, NONE_PROGRESS
from flask import Blueprint, render_template, redirect, url_for

app_home = Blueprint('app_home', __name__, template_folder='templates')
scraper_process: multiprocessing.Process = None

from flask import jsonify


@app_home.route('/ui/home')
def home():
    return render_template('home.html', logs=logger.get_application_logs(), trace_logs=logger.get_trace_logs())


@app_home.route('/ui/home/scraper/start')
def start_scraper():
    global scraper_process
    if scraper_process is None or not scraper_process.is_alive():
        scraper_process = multiprocessing.Process(target=start_scraper_process)
        scraper_process.start()
        progress_queue.put((NONE_PROGRESS, 'Starting scraper'))
    return redirect(url_for('app_home.home'))


@app_home.route('/ui/home/scraper/stop')
def stop_scraper():
    global scraper_process
    if scraper_process is not None and scraper_process.is_alive():
        scraper_process.kill()
        progress_queue.put((NONE_PROGRESS, 'Program finished with exit code 130', 'off'))
    return redirect(url_for('app_home.home'))

@app_home.route("/ui/home/test")
def test():
    return jsonify("""[ { title: "Start", type: "START", icon: "FastForwardIcon", index: 0 }, { title: "Mediterranean Avenue", type: "PROPERTY", color: "gray", price: 60, index: 1 }, { title: "Community Chest", type: "COMMUNITY", icon: "ArchiveIcon", index: 2 }, { title: "Baltic Avenue", type: "PROPERTY", color: "gray", price: 60, index: 3 }, { title: "Incoming tax", type: "TAX", icon: "ReceiptTaxIcon", price: 150, index: 4 }, { title: "Reading Railroad", type: "TRAIN_STATION", icon: "LibraryIcon", price: 200, index: 5 }, { title: "Oriental Avenue", type: "PROPERTY", color: "blue", price: 100, index: 6 }, { title: "Chance", type: "CHANCE", icon: "CashIcon", index: 7 }, { title: "Vermont Avenue", type: "PROPERTY", color: "blue", price: 100, index: 8 }, { title: "Connecticut Avenue", type: "PROPERTY", color: "blue", price: 120, index: 9 }, { title: "Jail", type: "JAIL", icon: "CubeTransparentIcon", index: 10 }, { title: "St. Charles Place", type: "PROPERTY", color: "purple", price: 140, index: 11 }, { title: "Electric Company", type: "TRAIN_STATION", icon: "LightningBoltIcon", price: 150, index: 12 }, { title: "States Avenue", type: "PROPERTY", color: "purple", price: 140, index: 13 }, { title: "Virginia Avenue", type: "PROPERTY", color: "purple", price: 160, index: 14 }, { title: "Pennsylvania Railroad", type: "TRAIN_STATION", icon: "LibraryIcon", price: 200, index: 15 }, { title: "St. James Place", type: "PROPERTY", color: "pink", price: 180, index: 16 }, { title: "Community Chest", type: "COMMUNITY", icon: "ArchiveIcon", index: 17 }, { title: "Tennessee Avenue", type: "PROPERTY", color: "pink", price: 180, index: 18 }, { title: "New York Avenue", type: "PROPERTY", color: "pink", price: 200, index: 19 }, { title: "Free Parking", type: "PARKING", icon: "LocationMarkerIcon", index: 20 }, { title: "Kentucky Avenue", type: "PROPERTY", color: "red", price: 220, index: 21 }, { title: "Chance", type: "CHANCE", icon: "CashIcon", index: 22 }, { title: "Indiana Avenue", type: "PROPERTY", color: "red", price: 220, index: 23 }, { title: "Illinois Avenue", type: "PROPERTY", color: "red", price: 240, index: 24 }, { title: "B&O Railroad", type: "TRAIN_STATION", icon: "LibraryIcon", price: 200, index: 25 }, { title: "Atlantic Avenue", type: "PROPERTY", color: "yellow", price: 260, index: 26 }, { title: "Ventnor Avenue", type: "PROPERTY", color: "yellow", price: 260, index: 27 }, { title: "Water Works", type: "TRAIN_STATION", icon: "BeakerIcon", price: 150, index: 28 }, { title: "Marvin Gardens", type: "PROPERTY", color: "yellow", price: 280, index: 29 }, { title: "Go To Jail", type: "GO_TO_JAIL", icon: "BanIcon", index: 30 }, { title: "Pacific Avenue", type: "PROPERTY", color: "green", price: 300, index: 31 }, { title: "North Carolina Avenue", type: "PROPERTY", color: "green", price: 300, index: 32 }, { title: "Community Chest", type: "COMMUNITY", icon: "ArchiveIcon", index: 33 }, { title: "Pennsylvania Avenue", type: "PROPERTY", color: "green", price: 320, index: 34 }, { title: "Short Line", type: "TRAIN_STATION", icon: "BeakerIcon", price: 150, index: 35 }, { title: "Chance", type: "CHANCE", icon: "CashIcon", index: 36 }, { title: "Park Place", type: "PROPERTY", color: "indigo", price: 350, index: 37 }, { title: "Luxury Tax", type: "TAX", icon: "ReceiptTaxIcon", price: 150, index: 38 }, { title: "Park Place", type: "PROPERTY", color: "indigo", price: 400, index: 39 } ] """)