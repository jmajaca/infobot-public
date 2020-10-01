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
    reaction_name: str = 'default'
        Name of reaction user wants to view, defaults to "default"

    Methods
    ----------
    get_top_senders(number_of_senders: int = default_number, reaction_name="default") -> str[]
        returns top number_of_senders reactions senders by number of sent reactions
    get_top_receivers(number_of_receivers: int = default_number, reaction_name="default") -> str[]
        returns top number_of_receivers reactions receivers by number of received reactions
    get_top_channels(number_of_channels: int = default_number, reaction_name="default") -> str[]
        returns top number_of_channels channels by reactions exchanged
    get_latest_reactions(number_of_top: int = default_number, reaction_name="default") -> tuple(sender, receiver, channel, time)
        returns tuple with information about latest reaction sender, receiver, channel and time of reaction exchange
    get_top_all(number_of_top: int = default_number, reaction_name="default")
        calls get_top_senders, get_top_receivers(), get_top_receivers(), get_top_channels(), get_latest_reactions()
    """

    default_number = 5

    def __init__(self, logger: Logger, default_number: int = default_number):
        self.session = Session()
        self.logger = logger
        self.default_number = default_number

    def get_top_senders(self, number_of_senders: int = default_number, reaction_name="default"):
        if reaction_name == "default":
            senders = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.sender == SlackUser.id).group_by(SlackUser.name).order_by(
                func.count(SlackUser.name).desc()).all()
        else:
            senders = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.sender == SlackUser.id).filter(Reaction.name == reaction_name).group_by(
                SlackUser.name).order_by(func.count(SlackUser.name).desc()).all()
        return senders[0:number_of_senders]

    def get_top_receivers(self, number_of_receivers: int = default_number, reaction_name="default"):
        if reaction_name == "default":
            receivers = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.receiver == SlackUser.id).group_by(SlackUser.name).order_by(
                func.count(SlackUser.name).desc()).all()
        else:
            receivers = self.session.query(SlackUser.name, func.count(SlackUser.name)).join(
                Reaction, Reaction.receiver == SlackUser.id).filter(Reaction.name == reaction_name).group_by(
                SlackUser.name).order_by(func.count(SlackUser.name).desc()).all()
        return receivers[0:number_of_receivers]

    def get_top_channels(self, number_of_channels: int = default_number, reaction_name="default"):
        if reaction_name == "default":
            top_channels = self.session.query(Channel.tag, func.count(Channel.tag)).join(
                Reaction, Reaction.channel == Channel.id).group_by(Channel.tag).order_by(
                func.count(Channel.tag).desc()).all()
        else:
            top_channels = self.session.query(Channel.tag, func.count(Channel.tag)).join(
                Reaction, Reaction.channel == Channel.id).filter(Reaction.name == reaction_name).group_by(
                Channel.tag).order_by(func.count(Channel.tag).desc()).all()
        return top_channels[0:number_of_channels]

    def get_latest_reactions(self, number_of_top: int = default_number, reaction_name="default"):
        slackUserR = aliased(SlackUser)
        slackUserS = aliased(SlackUser)
        if reaction_name == "default":
            latest_reactions = self.session.query(slackUserS.name, slackUserR.name, Channel.tag,
                                                  Reaction.timestamp).join(
                slackUserS, slackUserS.id == Reaction.sender).join(
                slackUserR, slackUserR.id == Reaction.receiver).join(Channel, Channel.id == Reaction.channel).all()
        else:
            latest_reactions = self.session.query(slackUserS.name, slackUserR.name, Channel.tag,
                                                  Reaction.timestamp).join(
                slackUserS, slackUserS.id == Reaction.sender).join(
                slackUserR, slackUserR.id == Reaction.receiver).join(Channel, Channel.id == Reaction.channel).filter(
                Reaction.name == reaction_name).all()

        for i in range(len(latest_reactions)):
            real_time = datetime.fromtimestamp(latest_reactions[i][3])
            latest_reactions[i] = latest_reactions[i][:3]
            latest_reactions[i] += (str(real_time)[:-7],)

        return latest_reactions[0:number_of_top]

    def get_top_all(self, number_of_top: int = default_number, reaction_name="default"):
        senders = self.get_top_senders(number_of_top, reaction_name)
        receivers = self.get_top_receivers(number_of_top, reaction_name)
        channels = self.get_top_channels(number_of_top, reaction_name)
        latest_reactions = self.get_latest_reactions(number_of_top, reaction_name)
        return senders, receivers, channels, latest_reactions
