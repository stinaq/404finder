class Link:
    """A link object holds the information about links

    Attributes:
        url: Self explanatory
        title: The text inside the anchor tag
        origin: The url to the page where the link was found
        content_type: The type of the link
    """
    def __init__(self, url, title, origin):
        self.url = url
        self.title = title
        self.origin = origin

    def __str__(self):
        return 'url: ' + self.url + ', title: ' + self.title + ', origin: ' + self.origin

    def __repr__(self):
        return 'url: ' + self.url + ', title: ' + self.title + ', origin: ' + self.origin
