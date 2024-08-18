from blog.models import Article, Category
from modeltranslation.translator import TranslationOptions, register


@register(Article)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('Title', 'Description')


@register(Category)
class ArticleTranslationOptions(TranslationOptions):
    fields = ('titles',)
