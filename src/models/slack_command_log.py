from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, TIMESTAMP, Boolean
from src.models.base import Base


class SlackCommandLog(Base):
    __tablename__ = 'slack_command_log'
    id = Column(Integer, Sequence('slack_command_log_id_seq'), primary_key=True)
    text = Column(String, nullable=True)
    command = Column(String, nullable=False)
    creation_time = Column(TIMESTAMP, nullable=False)
    channel_id = Column(String, ForeignKey('channel.id'), nullable=False)
    user_id = Column(String, ForeignKey('slack_user.id'), nullable=False)
    success = Column(Boolean, nullable=False)

    def __init__(self, text, command, creation_time, channel_id, user_id, success):
        self.text, self.command, self.creation_time, self.channel_id, self.user_id, self.success = text, command, creation_time, channel_id, user_id, success

    def __repr__(self):
        return ("<SlackCommandLog(id='%s', command='%s', text='%s', creation_time='%s', channel_id='%s', user_id='%s', success='%s')>" %
                (str(self.id), self.command, self.text, str(self.creation_time), self.channel_id, self.user_id, self.success))
