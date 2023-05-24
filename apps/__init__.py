from .author.views import router as author
from .book.views import router as book


routers = [author, book]