from .renderers import DjangoTemplates
from .utils import ErrorList
from django.forms import forms 


class PrettyFormMixin:
    default_renderer = DjangoTemplates()
    template_name_div = "pretty/div.html"
    template_name_p = "pretty/p.html"
    template_name_table = "pretty/table.html"
    template_name_ul = "pretty/ul.html"
    template_name_label = "pretty/label.html"


class BaseForm(PrettyFormMixin, forms.BaseForm):
    def __init__(
        self,
        data=None,
        files=None,
        auto_id="id_%s",
        prefix=None,
        initial=None,
        error_class=ErrorList,
        label_suffix=None,
        empty_permitted=False,
        field_order=None,
        use_required_attribute=None,
        renderer=None,
    ):
        super().__init__(data=data, files=files, auto_id=auto_id, prefix=None,
                error_class=error_class, label_suffix=label_suffix,
                empty_permitted=empty_permitted, field_order=field_order,
                use_required_attribute=use_required_attribute, 
                renderer=renderer, initial=initial)

class Form(BaseForm, metaclass=forms.DeclarativeFieldsMetaclass):
    pass
