from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'


class SuitConfig(DjangoSuitConfig):
    layout = 'horizontal'