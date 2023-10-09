class MenuItem:
    url: str
    name: str

    def __init__(self, url: str, name: str=None):
        self.url = url
        self.name = name or url
