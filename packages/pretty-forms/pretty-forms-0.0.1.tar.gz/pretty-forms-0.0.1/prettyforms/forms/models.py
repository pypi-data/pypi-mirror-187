from itertools import chain
from django.forms import models as forms_models
from django.forms.forms import DeclarativeFieldsMetaclass
from django.db import models
from bulmaforms.forms.renderers import DjangoTemplates
from bulmaforms.forms.utils import ErrorList
from bulmaforms.forms import widgets
from bulmaforms.forms import forms as bulmaforms
from bulmaforms.forms import fields as bulmafields


EQUIVALENCES_MODEL_FORM = {
    models.TextField: bulmafields.TextField,
    models.CharField: bulmafields.CharField,
    models.IntegerField: bulmafields.IntegerField,
    models.FloatField: bulmafields.FloatField,
    models.DateField: bulmafields.DateField,
    models.TimeField: bulmafields.TimeField,
    models.DateTimeField: bulmafields.DateTimeField,
    models.DurationField: bulmafields.DurationField,
    models.EmailField: bulmafields.EmailField,
    models.FileField: bulmafields.FileField,
    models.ImageField: bulmafields.ImageField,
    models.BooleanField: bulmafields.BooleanField,
    models.ManyToManyField: bulmafields.MultipleChoiceField,
    }


def formfield_callback(model_field, **kwargs):
    cls = model_field.__class__
    if cls == models.TextField:
        ff = model_field.formfield(form_class=bulmafields.TextField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
        ff.widget = widgets.Textarea(**kwargs)
        return ff
    elif cls == models.CharField:
        return model_field.formfield(form_class=bulmafields.CharField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.DecimalField:
        return model_field.formfield(form_class=bulmafields.DecimalField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.IntegerField:
        return model_field.formfield(form_class=bulmafields.IntegerField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.BigAutoField:
        return model_field.formfield(form_class=bulmafields.IntegerField, 
                **kwargs)
    elif cls == models.PositiveIntegerField:
        return model_field.formfield(form_class=bulmafields.PositiveIntegerField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.FloatField:
        return model_field.formfield(form_class=bulmafields.FloatField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.DateField:
        return model_field.formfield(form_class=bulmafields.DateField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.TimeField:
        return model_field.formfield(form_class=bulmafields.TimeField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.DateTimeField:
        return model_field.formfield(form_class=bulmafields.DateTimeField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.DurationField:
        return model_field.formfield(form_class=bulmafields.DurationField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.EmailField:
        return model_field.formfield(form_class=bulmafields.EmailField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.FileField:
        return model_field.formfield(form_class=bulmafields.FileField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.ImageField:
        return model_field.formfield(form_class=bulmafields.ImageField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.BooleanField:
        return model_field.formfield(form_class=bulmafields.BooleanField, 
                choices_form_class=bulmafields.TypedChoiceField, **kwargs)
    elif cls == models.ManyToManyField:
        return model_field.formfield(form_class=ModelMultipleChoiceField,
                **kwargs)
    elif cls == models.ForeignKey:
        return model_field.formfield(form_class=ModelChoiceField,
                **kwargs)
    else:
        print("No traga " + str(cls))
        return None

def fields_for_model(
    model,
    fields=None,
    exclude=None,
    widgets=None,
    localized_fields=None,
    labels=None,
    help_texts=None,
    error_messages=None,
    field_classes=None,
    *,
    apply_limit_choices_to=True,
):
    """
    Return a dictionary containing form fields for the given model.

    ``fields`` is an optional list of field names. If provided, return only the
    named fields.

    ``exclude`` is an optional list of field names. If provided, exclude the
    named fields from the returned fields, even if they are listed in the
    ``fields`` argument.

    ``widgets`` is a dictionary of model field names mapped to a widget.

    ``localized_fields`` is a list of names of fields which should be localized.

    ``labels`` is a dictionary of model field names mapped to a label.

    ``help_texts`` is a dictionary of model field names mapped to a help text.

    ``error_messages`` is a dictionary of model field names mapped to a
    dictionary of error messages.

    ``field_classes`` is a dictionary of model field names mapped to a form
    field class.

    ``apply_limit_choices_to`` is a boolean indicating if limit_choices_to
    should be applied to a field's queryset.
    """

    field_dict = {}
    ignored = []
    opts = model._meta
    # Avoid circular import
    from django.db.models import Field as ModelField

    sortable_private_fields = [
        f for f in opts.private_fields if isinstance(f, ModelField)
    ]
    for f in sorted(
        chain(opts.concrete_fields, sortable_private_fields, opts.many_to_many)
    ):
        if not getattr(f, "editable", False):
            if (
                fields is not None
                and f.name in fields
                and (exclude is None or f.name not in exclude)
            ):
                raise FieldError(
                    "'%s' cannot be specified for %s model form as it is a "
                    "non-editable field" % (f.name, model.__name__)
                )
            continue
        if fields is not None and f.name not in fields:
            continue
        if exclude and f.name in exclude:
            continue

        kwargs = {}
        if widgets and f.name in widgets:
            kwargs["widget"] = widgets[f.name]
        if localized_fields == forms_models.ALL_FIELDS or (
            localized_fields and f.name in localized_fields
        ):
            kwargs["localize"] = True
        if labels and f.name in labels:
            kwargs["label"] = labels[f.name]
        if help_texts and f.name in help_texts:
            kwargs["help_text"] = help_texts[f.name]
        if error_messages and f.name in error_messages:
            kwargs["error_messages"] = error_messages[f.name]
        if field_classes and f.name in field_classes:
            kwargs["form_class"] = field_classes[f.name]


        formfield = formfield_callback(f, **kwargs)

        if formfield:
            if apply_limit_choices_to:
                apply_limit_choices_to_to_formfield(formfield)
            field_dict[f.name] = formfield
        else:
            ignored.append(f.name)
    if fields:
        field_dict = {
            f: field_dict.get(f)
            for f in fields
            if (not exclude or f not in exclude) and f not in ignored
        }
    return field_dict


class ModelFormMetaclass(DeclarativeFieldsMetaclass):
    def __new__(mcs, name, bases, attrs):
        new_class = super().__new__(mcs, name, bases, attrs)

        if bases == (BaseModelForm,):
            return new_class

        opts = new_class._meta = forms_models.ModelFormOptions(getattr(new_class, "Meta", None))

        # We check if a string was passed to `fields` or `exclude`,
        # which is likely to be a mistake where the user typed ('foo') instead
        # of ('foo',)
        for opt in ["fields", "exclude", "localized_fields"]:
            value = getattr(opts, opt)
            if isinstance(value, str) and value != ALL_FIELDS:
                msg = (
                    "%(model)s.Meta.%(opt)s cannot be a string. "
                    "Did you mean to type: ('%(value)s',)?"
                    % {
                        "model": new_class.__name__,
                        "opt": opt,
                        "value": value,
                    }
                )
                raise TypeError(msg)

        if opts.model:
            # If a model is defined, extract form fields from it.
            if opts.fields is None and opts.exclude is None:
                raise ImproperlyConfigured(
                    "Creating a ModelForm without either the 'fields' attribute "
                    "or the 'exclude' attribute is prohibited; form %s "
                    "needs updating." % name
                )

            if opts.fields == forms_models.ALL_FIELDS:
                # Sentinel for fields_for_model to indicate "get the list of
                # fields from the model"
                opts.fields = None

            fields = fields_for_model(
                opts.model,
                opts.fields,
                opts.exclude,
                opts.widgets,
                opts.localized_fields,
                opts.labels,
                opts.help_texts,
                opts.error_messages,
                opts.field_classes,
                # limit_choices_to will be applied during ModelForm.__init__().
                apply_limit_choices_to=False,
            )

            # make sure opts.fields doesn't specify an invalid field
            none_model_fields = {k for k, v in fields.items() if not v}
            missing_fields = none_model_fields.difference(new_class.declared_fields)
            if missing_fields:
                message = "Unknown field(s) (%s) specified for %s"
                message %= (", ".join(missing_fields), opts.model.__name__)
                raise FieldError(message)
            # Override default model fields with any custom declared ones
            # (plus, include all the other declared fields).
            fields.update(new_class.declared_fields)
        else:
            fields = new_class.declared_fields

        new_class.base_fields = fields

        return new_class




class BaseModelForm(bulmaforms.BulmaFormMixin, forms_models.BaseModelForm):
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
        instance=None,
        use_required_attribute=None,
        renderer=None,
    ):
        opts = self._meta
        if opts.model is None:
            raise ValueError("ModelForm has no model class specified.")
        if instance is None:
            # if we didn't get an instance, instantiate a new one
            self.instance = opts.model()
            object_data = {}
        else:
            self.instance = instance
            object_data = forms_models.model_to_dict(instance, opts.fields, opts.exclude)
        # if initial was provided, it should override the values from instance
        if initial is not None:
            object_data.update(initial)
        # self._validate_unique will be set to True by BaseModelForm.clean().
        # It is False by default so overriding self.clean() and failing to call
        # super will stop validate_unique from being called.
        self._validate_unique = False
        super().__init__(
            data,
            files,
            auto_id,
            prefix,
            object_data,
            error_class,
            label_suffix,
            empty_permitted,
            use_required_attribute=use_required_attribute,
            renderer=renderer,
        )
        for formfield in self.fields.values():
            forms_models.apply_limit_choices_to_to_formfield(formfield)


class ModelForm(BaseModelForm, metaclass=ModelFormMetaclass):
    pass


class ModelChoiceIterator(forms_models.ModelChoiceIterator):
    pass


class InlineForeignKeyField(forms_models.InlineForeignKeyField):
    widget = widgets.HiddenInput


class ModelChoiceField(forms_models.ModelChoiceField):
    widget = widgets.Select
    

class ModelMultipleChoiceField(forms_models.ModelChoiceField):
    widget = widgets.SelectMultiple
    hidden_widget = widgets.MultipleHiddenInput
