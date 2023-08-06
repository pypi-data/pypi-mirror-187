import functools
from pathlib import Path
from django.forms import renderers
from django.template.backends.django import DjangoTemplates as DTS
from django.utils.functional import cached_property

@functools.lru_cache
def get_default_renderer():
    return DjangoTemplates()


class BaseRenderer(renderers.BaseRenderer):
    form_template_name = "bulma/default.html"
    formset_template_name = "bulma/formsets/default.html"


class EngineMixin:
    def get_template(self, template_name):
        return self.engine.get_template(template_name)

    @cached_property
    def engine(self):
        return self.backend(
                {
                    "APP_DIRS": True,
                    "DIRS": [Path(__file__).parent.parent / "templates"],
                    "NAME": "bulmaforms",
                    "OPTIONS": {},
                    }
                )


class DjangoTemplates(EngineMixin, BaseRenderer):
        backend = DTS


class DjangoDivFormRenderer(DjangoTemplates):
    form_template_name = "bulma/div.html"
    formset_template_name = "bulma/formsets/div.html"
