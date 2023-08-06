from django.forms.utils import RenderableFormMixin, ErrorDict as DjangoErrorDict, ErrorList as DjangoErrorList
from .renderers import DjangoTemplates

class ErrorDict(DjangoErrorDict):
    template_name = 'bulma/errors/dict/default.html'
    template_name_text = 'bulma/errors/dict/text.txt'
    template_name_ul = 'bulma/errors/dict/ul.html'

    def __init__(self, *args, renderer=DjangoTemplates(), **kwargs):
        super().__init__(*args, **kwargs)


class ErrorList(DjangoErrorList):
    template_name = 'bulma/errors/list/default.html'
    template_name_text = 'bulma/errors/list/text.txt'
    template_name_ul = 'bulma/errors/list/ul.html'

    def __init__(self, initlist=None, error_class=None, 
            renderer=DjangoTemplates()):
        super().__init__(initlist=initlist, error_class=error_class,
                renderer=renderer)
