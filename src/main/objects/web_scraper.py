import re
import time

import requests

from datetime import datetime
from bs4 import BeautifulSoup

from src import errors, Logger
from src.main.objects.helper_objects import LinkHelper
from src.main.objects.progress_queue_manager import ProgressQueueManager
from src.models.author import Author
from src.models.base import DataBase
from src.models.course import Course
from src.models.notification import Notification


class WebScraper:
    """
    A class that scrapes FER Web for notifications

    Attributes
    ----------
    database: DataBase
        a object that is responsible for communicating with database
    progress_queue_manager: ProgressQueueManager
        a object that is responsible for keeping track of progress made while scraping notifications
    logger : Logger
        a object that is saving scanner logs to a predefined file
    link : str
        a link to FER web page from which data will be scrapped
    payload: dict
        a dictionary that contains payload (like username and password) for logging into target website
    date_format: dict
        a dictionary that contains date formats found in web notifications
    headers: dict
        optional dictionary that is sent as HTTP header when scraping
    html_parser: str
        optional parameter that defines which html parser to use when parsing scraped raw HTML

    Methods
    -------
    start(courses: list[Course]) -> list[Notification]
        starts wrapped process of scraping notifications for target courses
    generate_notifications(courses: list[Course]) -> list[Notification]
        scraping notifications for target courses
    _check_author(author_string: str) -> Author
        checks for author and saves it to database if author doesn't exists
    _check_date(date_elements: list)
        returns most recent date object based on date_format
    _check_text(text: str) -> str
        parsing text for Slack message
    """

    def __init__(self, link: str, payload: dict, **kwargs):
        self.database = DataBase()
        self.progress_queue_manager = ProgressQueueManager()
        self.logger = Logger()
        self.link = link
        self.payload = payload
        self.date_format = {
            'small': '%Y-%m-%dT%H:%M',
            'medium': '%Y-%m-%dCET%H:%M',
            'large': '%Y-%m-%dCEST%H:%M'
        }
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.html_parser = 'html.parser'
        if kwargs and 'headers' in kwargs:
            self.headers = kwargs['headers']
        if kwargs and 'html_parser' in kwargs:
            self.html_parser = kwargs['html_parser']

    def start(self, courses):
        notifications = []
        try:
            notifications = self.generate_notifications(courses)
        except errors.LoginError as e:
            notifications = None
            self.logger.warning_log(e.text)
        except Exception as e:
            notifications = []
            self.logger.error_log(e, text='Error has occurred while scraping notifications ')
        finally:
            return notifications

    def generate_notifications(self, courses):
        notifications = []
        session = requests.Session()
        intranet = session.post(self.link + '/login', headers=self.headers, data=self.payload)
        soup = BeautifulSoup(intranet.text, self.html_parser)
        check_element = soup.find('li', {'class': 'home-page'})
        if not check_element.text.__contains__('Intranet'):
            raise errors.LoginError
        self.progress_queue_manager.init_phase()
        for i, course in enumerate(courses):
            time.sleep(2)
            self.progress_queue_manager.scraping_course_start_info(course)
            link = course.url + '/obavijesti'
            raw_html = session.get('https://' + link, headers=self.headers, data=self.payload).text
            soup = BeautifulSoup(raw_html, self.html_parser)
            news_articles = soup.findAll('div', {'class': 'news_article'})
            for j, news_article in enumerate(news_articles):
                title_element = news_article.find('div', {'class': 'news_title'})
                notification = Notification()
                notification.link = self.link + title_element.a['href']
                notification.title = title_element.get_text().strip()
                notification.site = self.database.select(Course, name=course.name).id
                notification.author = self._check_author(news_article
                                                         .find('span', {'class': 'author_name'})
                                                         .get_text().strip()).id
                notification.publish_date = self._check_date(news_article.findAll('time'))
                notification.text = self._check_text(str(news_article.find('div', {'class': 'news_lead'}))
                                                     .replace('<p>', '').replace('</p>', '\n'))
                notifications.append(notification)
                self.progress_queue_manager.scrape_phase(course, i, j, len(courses), len(news_articles))
            self.progress_queue_manager.scraping_course_done_info(course, i, len(courses))
        session.get(self.link + '/login/Logout?logout=1')
        return notifications

    def _check_author(self, author_string: str) -> Author:
        author_name_list = author_string.split()
        author = self.database.select(Author, first_name=author_name_list[0], last_name=' '.join(author_name_list[1:]))
        if author is None:
            self.database.insert(Author(author_name_list[0], ' '.join(author_name_list[1:])))
            author = self.database.select(Author, first_name=author_name_list[0],
                                          last_name=' '.join(author_name_list[1:]))
        return author

    def _check_date(self, date_elements: list):
        date = None
        for date_element in date_elements:
            element = date_element['datetime']
            if len(element) == 16:
                iteration_date = datetime.strptime(element, self.date_format['small'])
            elif len(element) == 18:
                iteration_date = datetime.strptime(element, self.date_format['medium'])
            else:
                iteration_date = datetime.strptime(element, self.date_format['large'])
            if date is None:
                date = iteration_date
            elif date < iteration_date:
                # if date was edited get most recent date
                date = iteration_date
        return date

    # https://api.slack.com/reference/surfaces/formatting
    def _check_text(self, text: str) -> str:
        # getting only text from html
        text = '\n'.join(text.split('\n')[1:-1]).strip()
        # replacing HTML spacing
        text = text.replace(u"\u00A0", " ")
        # closing right gaps
        text = re.sub(r'([0-9A-z:;,"\').]) +(</)', r'\g<1>\g<2>', text)
        # closing left gaps
        text = re.sub(r'(<[^>]+>) +([^ ])', r'\g<1>\g<2>', text)
        # expanding right gaps
        text = re.sub(r'(</[^>]+>)([^ :;,"\').])', r'\g<1> \g<2>', text)
        # expanding left gaps
        text = re.sub(r'([^ :;"\'(.])(<[^/>]+>)', r'\g<1> \g<2>', text)
        # replacing bold and italic html tags for slack tags
        text = text.replace('<strong>', '*').replace('</strong>', '*').replace('<em>', '_').replace('</em>', '_')
        # parsing links
        link_groups: list[LinkHelper] = LinkHelper.create_list(
            re.findall(r'(<a href=\"([^<> ]*)\"[^<>]*>([^<>]*)</a>)', text))
        for link_group in link_groups:
            if 'http' in link_group.target:
                text = re.sub(re.escape(link_group.target), '&lt;' + link_group.link + '|' + link_group.text + '&gt;',
                              text)
            else:
                mail_elements = re.search(r"javascript:cms_mail\(\'([^,]*)\',\'([^,]*)\'.*\)", link_group.link)
                text = re.sub(re.escape(link_group.target), '&lt;mailto:' + mail_elements.group(1) + '@' +
                              mail_elements.group(2) + '|' + link_group.text + '&gt;', text)
        # workaround for Slack not parsing list as expected
        text = text.replace('<li>', '<li>• ')
        # removing extra spaces
        text = re.sub(r' +', r' ', text)
        # parsing the rest of text
        return BeautifulSoup(text, self.html_parser).get_text()
