import logging

from sorl.thumbnail.log import ThumbnailLogHandler

handler = ThumbnailLogHandler()
handler.setLevel(logging.ERROR)
logging.getLogger("sorl.thumbnail").addHandler(handler)
