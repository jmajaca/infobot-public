import re
import time

import requests

from datetime import datetime
from bs4 import BeautifulSoup
from src import errors, progress_queue, INIT_PROGRESS, SCRAPE_PROGRESS
from src import logger
from src.main.helper import create_notification_object


class Scraper:

    def __init__(self, link, payload, **kwargs):
        self.link = link
        self.payload = payload
        self.headers = {'User-Agent': 'Mozilla/5.0'}
        self.html_parser = 'html.parser'
        if kwargs:
            if 'headers' in kwargs:
                self.headers = kwargs['headers']
            if 'html_parser' in kwargs:
                self.html_parser = kwargs['html.parser']

    def scrape_notifications(self, courses):
        notifications = []
        try:
            notifications = generate_notifications(self.link, self.payload, self.html_parser, self.headers, courses)
        except errors.LoginError as e:
            notifications = None
            logger.warning_log(e.text)
        except Exception as e:
            notifications = []
            logger.error_log(e, text='Error has occurred while scraping notifications ')
        finally:
            return notifications


# https://www.crummy.com/software/BeautifulSoup/bs4/doc/
def generate_notifications(fer_url, payload, html_parser, headers, courses):
    info = []
    session = requests.Session()
    intranet = session.post(fer_url + '/login', headers=headers, data=payload)
    soup = BeautifulSoup(intranet.text, html_parser)
    check_element = soup.find('li', {'class': 'home-page'})
    if not check_element.text.__contains__('Intranet'):
        raise errors.LoginError
    progress_queue.put((INIT_PROGRESS, 'Setup done'))
    course_progress = int(SCRAPE_PROGRESS / (len(courses)))
    for i in range(len(courses)):
        time.sleep(2)
        course = courses[i]
        progress_queue.put((None, 'Scraping course \'%s\'' % course.name))
        link = course.url + '/obavijesti'
        notification = dict()
        raw_html = session.get('https://' + link, headers=headers, data=payload).text
        soup = BeautifulSoup(raw_html, html_parser)
        news_articles = soup.findAll('div', {'class': 'news_article'})
        for j in range(len(news_articles)):
            news_article = news_articles[j]
            title_element = news_article.find('div', {'class': 'news_title'})
            notification['link'] = fer_url + title_element.a['href']
            notification['title'] = title_element.get_text().rstrip().lstrip()
            notification['site_name'] = course.name
            notification['author_name'] = news_article.find('span',
                                                            {'class': 'author_name'}).get_text().rstrip().lstrip()
            date = None
            for el in news_article.findAll('time'):
                if len(el['datetime']) == 16:
                    tmp_date = datetime.strptime(el['datetime'], '%Y-%m-%dT%H:%M')
                elif len(el['datetime']) == 18:
                    tmp_date = datetime.strptime(el['datetime'], '%Y-%m-%dCET%H:%M')
                else:
                    tmp_date = datetime.strptime(el['datetime'], '%Y-%m-%dCEST%H:%M')
                if date is None:
                    date = tmp_date
                else:
                    if date < tmp_date:
                        date = tmp_date
            notification['date'] = date
            text = str(news_article.find('div', {'class': 'news_lead'})).replace('<p>', '').replace('</p>', '\n')
            text = '\n'.join(text.split('\n')[1:-1]).lstrip().rstrip()
            text = text.replace('<strong>', ' *').replace('</strong>', '* ').replace('<em>', ' ■').replace('</em>',
                                                                                                           '■ ')
            # https://api.slack.com/reference/surfaces/formatting#linking_to_urls
            text_links = re.findall(r'((?:[^<>]*)<a href=\"([^<> ]*)\"[^<>]*>([^<>]*)</a>)', text)
            for text_link in text_links:
                if re.search(r'http.*', text_link[1]):
                    text = re.sub(pattern=re.compile('<a href=\"' + text_link[1] + '\"[^<>]*>([^<>]*)</a>'),
                                  string=text, repl='&lt;'
                                                    + text_link[1] + '|' + text_link[2] + '&gt;')
                else:
                    text = re.sub(pattern=re.compile('<a href=\"' + text_link[1] + '\"[^<>]*>([^<>]*)</a>'),
                                  string=text, repl='&lt;mailto:'
                                                    + text_link[2] + '|' + text_link[2] + '&gt;')
            text = text.replace('<li>', '<li>• ')
            text = text.replace('  ', ' ')
            text = BeautifulSoup(text, html_parser).get_text()
            notification['text'] = tune_italic_bold(text)
            info.append(create_notification_object(notification))
            progress_queue.put((INIT_PROGRESS + course_progress * i + int(course_progress/len(news_articles)) * (j+1),
                                'Scraping course \'%s\'' % course.name))
        progress_queue.put((INIT_PROGRESS + course_progress * (i+1), 'Scraping course \'%s\' done' % course.name))
    session.get(fer_url + '/login/Logout?logout=1')
    return info


def tune_italic_bold(text):
    # first - on the start of line, second - in the middle of line
    text = tune_text(text, re.findall(r'.?\*[^*]+\*.', text), '*')
    text = tune_text(text, re.findall(r'.?■[^■]+■.', text), '■')
    # TODO this is specific
    # if re.findall(re.compile('(■[a-z\.0-9]+@[a-z]+\.[a-z]{2,3})'), text):
    #     for mail in re.findall(re.compile('(■[a-z\.0-9]+@[a-z]+\.[a-z]{2,3})'), text):
    #         text = re.sub(pattern=re.escape(mail[0]), string=text, repl='■⠀' + mail[0][1:])
    text = text.replace('■', '_')
    return text


def tune_text(text, matches, char):
    for element in matches:
        pattern = element
        # * pattern
        if element[2] == ' ':
            element = element[0:2] + element[3:]
        # i*pattern => i *pattern
        # if element[0] == char than it is start of the line
        if element[0] != ' ' and element[0] != char:
            element = element[0] + ' ' + element[1:]
        # pattern *
        if element[-3] == ' ':
            element = element[:-3] + element[-2:]
        # pattern *i | pattern*i
        if element[-1] != ' ':
            element = element[:-2] + ' ' + element[-1]
        # if somebody put ' * * ' => ' ** '
        if element == (' ' + char + char + ' '):
            element = ' '
        text = re.sub(pattern=re.escape(pattern), string=text, repl=element)
    return text
