
import datetime
import locale
locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')


class Post:
    def __init__(self, author, author_id, text, media=[]):

        self.Author = author
        self.authorid = author_id
        self.text = text
        self.media = media

        self.isOnlyText = False if len(media) > 0 else True

        self.created = datetime.datetime.today().strftime("%c")
        self.priority = 0

        self.Is_accepted = False
        self.acceptedAdmin = ""

        self.IsDel = False

