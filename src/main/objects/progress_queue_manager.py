from src import progress_queue
from src.models.course import Course


class ProgressQueueManager:
    """
    A manager object that is responsible for keeping track of scraping process

    Attributes
    ----------
    queue: str
        queue that stores information about scraping progress
    progress: dict
        a dictionary that contains progress keywords and its values

    Methods
    -------
    init_phase()
        puts init progress in queue
    scraping_course_start_info(course: Course)
        puts message about starting scraping for course in queue
    scraping_course_done_info(course: Course, current_course_index: int, courses_num: int)
        puts message about starting scraping for course in queue with dynamically calculated progress
    scrape_phase(course: Course, current_course_index: int, current_notification_index: int, courses_num: int,
                 notifications_num: int)
        dynamically calculates progress based on current course and current notification out of total and together with
        message stores it in progress queue
    _put_in_queue(key, value)
        method for putting value under key in progress queue
    """

    def __init__(self):
        self.queue = progress_queue
        self.progress = {
            'none': 0,
            'init': 5,
            'scrape': 80,
            'save': 15,
            'done': 100,
            None: None
        }

    def init_phase(self):
        self._put_in_queue('init', 'Setup done')

    def scraping_course_start_info(self, course: Course):
        self._put_in_queue(None, 'Scraping course \'%s\'' % course.name)

    def scraping_course_done_info(self, course: Course, current_course_index: int, courses_num: int):
        course_progress = int(self.progress['scrape'] / courses_num)
        progress_queue.put((self.progress['init'] + course_progress * (current_course_index + 1),
                            'Scraping course \'%s\' done' % course.name))

    def scrape_phase(self, course: Course, current_course_index: int, current_notification_index: int, courses_num: int,
                     notifications_num: int):
        course_progress = int(self.progress['scrape'] / courses_num)
        self.queue.put((self.progress['init'] + course_progress * current_course_index +
                        int(course_progress / notifications_num) * (current_notification_index + 1),
                        'Scraping course \'%s\'' % course.name))

    def _put_in_queue(self, key, value):
        self.queue.put((self.progress[key], value))
