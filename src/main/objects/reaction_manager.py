from sqlalchemy import func
from sqlalchemy.orm import aliased

from src.models.base import Session
from datetime import datetime
from multiprocessing import Process
from src import Logger
from src.models.model_list import Reaction, SlackUser, Channel


class ReactionManager:
    """
    A class responsible for handling all actions related to reactions in database

    Attributes
    ----------
    logger : Logger
        a object that is saving scanner logs to a predefined file
    default_number: int
        the number of senders/receivers/channels etc. that will be selected for display
    search_filter: String
        Name of reaction user wants to view, defaults to "default"
    """

    default_number = 5

    def __init__(self, logger: Logger, default_number: int = default_number):
        self.session = Session()
        self.logger = logger
        self.default_number = default_number

    def get_top_senders(self, number_of_senders: int = default_number, search_filter="default"):
        if search_filter == "default":
            senders = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.sender == SlackUser.id).group_by(SlackUser.name).order_by(
                func.count(SlackUser.name).desc()).all()
        else:
            senders = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.sender == SlackUser.id).filter(Reaction.name == search_filter).group_by(
                SlackUser.name).order_by(func.count(SlackUser.name).desc()).all()
        # self.logger.info_log("Retrieved top senders.")
        return senders[0:number_of_senders]

    def get_top_receivers(self, number_of_receivers: int = default_number, search_filter="default"):
        if search_filter == "default":
            receivers = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.receiver == SlackUser.id).group_by(SlackUser.name).order_by(
                func.count(SlackUser.name).desc()).all()
        else:
            receivers = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.receiver == SlackUser.id).filter(Reaction.name == search_filter).group_by(
                SlackUser.name).order_by(func.count(SlackUser.name).desc()).all()
        # self.logger.info_log("Retrieved top receivers.")
        return receivers[0:number_of_receivers]

    def get_top_channels(self, number_of_channels: int = default_number, search_filter="default"):
        if search_filter == "default":
            top_channels = self.session.query(Channel.tag, func.count(Channel.tag)).join(
                Reaction, Reaction.channel == Channel.id).group_by(Channel.tag).order_by(
                func.count(Channel.tag).desc()).all()
        else:
            top_channels = self.session.query(Channel.tag, func.count(Channel.tag)).join(
                Reaction, Reaction.channel == Channel.id).filter(Reaction.name == search_filter).group_by(
                Channel.tag).order_by(func.count(Channel.tag).desc()).all()
        # self.logger.info_log("Retrieved top channels.")
        return top_channels[0:number_of_channels]

    def get_latest_reactions(self, number_of_top: int = default_number, search_filter="default"):
        slackUserR = aliased(SlackUser)
        slackUserS = aliased(SlackUser)
        if search_filter == "default":
            latest_reactions = self.session.query(slackUserS.name, slackUserR.name, Channel.tag,
                                                  Reaction.timestamp).join(slackUserS,
                                                                           slackUserS.id == Reaction.sender). \
                join(slackUserR, slackUserR.id == Reaction.receiver).join(Channel, Channel.id == Reaction.channel).\
                all()
        else:
            latest_reactions = self.session.query(slackUserS.name, slackUserR.name, Channel.tag,
                                                  Reaction.timestamp).join(slackUserS, slackUserS.id == Reaction.sender).\
                join(slackUserR, slackUserR.id == Reaction.receiver).join(Channel, Channel.id == Reaction.channel)\
                .filter(Reaction.name == search_filter).all()

        for i in range(len(latest_reactions)):
            real_time = datetime.fromtimestamp(latest_reactions[i][3])
            latest_reactions[i] = latest_reactions[i][:3]
            latest_reactions[i] += (str(real_time)[:-7],)

        return latest_reactions[0:number_of_top]

    def get_top_all(self, number_of_top: int = default_number, search_filter="default"):
        senders = self.get_top_senders(number_of_top, search_filter)
        receivers = self.get_top_receivers(number_of_top, search_filter)
        channels = self.get_top_channels(number_of_top, search_filter)
        latest_reactions = self.get_latest_reactions(number_of_top, search_filter)
        return senders, receivers, channels, latest_reactions
