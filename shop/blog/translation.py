from blog.models import Article
from modeltranslation.translator import TranslationOptions , register

@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('Title' , 'Description'  )