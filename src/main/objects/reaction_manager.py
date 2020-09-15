from sqlalchemy import func
from src.models.base import Session
from datetime import datetime
from multiprocessing import Process
from src import Logger
from src.models.model_list import Reaction, SlackUser


class ReactionManager:
    """
    A class responsible for handling all actions related to reactions in database

    Attributes
    ----------
    logger : Logger
        a object that is saving scanner logs to a predefined file
    default_number: int
        the number of senders/receivers/channels etc. that will be selected for display

    """
    def __init__(self, logger: Logger, default_number: int = 5):
        self.session = Session()
        self.logger = logger
        self.default_number = default_number

    def get_top_senders(self, number_of_senders: int = 5):
        senders = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
            Reaction, Reaction.sender == SlackUser.id).group_by(SlackUser.name).all()
        self.logger.info_log("Retrieved top senders.")
        return senders[0:number_of_senders]

    def get_top_receivers(self, number_of_receivers: int = 5):
        receivers = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
            Reaction, Reaction.receiver == SlackUser.id).group_by(SlackUser.name).all()
        self.logger.info_log("Retrieved top receivers.")
        return receivers[0:number_of_receivers]
