class LinkHelper:
    """
    A helper class for storing link data from raw text notification

    Attributes
    ----------
    target: str
        whole match string that contains link and text attribute
    link: str
        link from target
    text: str
        text that is shown instead of link in message

    Methods
    -------
    create_list(groups: list) -> list[LinkHelper]
        creating list of ListHelper objects
    """

    def __init__(self, target, link, text):
        self.target, self.link, self.text = target, link, text

    @staticmethod
    def create_list(groups: list) -> list:
        return [LinkHelper(*group) for group in groups]
