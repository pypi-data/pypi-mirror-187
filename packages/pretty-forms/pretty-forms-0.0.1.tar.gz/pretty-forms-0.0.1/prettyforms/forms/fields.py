from bulmaforms.forms import widgets
from django.forms import fields
from django.forms.fields import DateTimeFormatsIterator, CallableChoiceIterator

"""
Estos son para usarlos directamente en formularios manuales
"""


class Field(fields.Field):
    widget = widgets.TextInput


class CharField(fields.CharField):
    widget = widgets.TextInput


class TextField(fields.CharField):
    widget = widgets.Textarea


class IntegerField(fields.IntegerField):
    widget = widgets.NumberInput


class PositiveIntegerField(fields.IntegerField):
    widget = widgets.NumberInput


class FloatField(fields.FloatField):
    widget = widgets.NumberInput


class DecimalField(fields.DecimalField):
    widget = widgets.NumberInput


class DateField(fields.DateField):
    widget = widgets.DateInput


class TimeField(fields.TimeField):
    widget = widgets.TimeInput


class DateTimeField(fields.DateTimeField):
    widget = widgets.DateTimeInput


class DurationField(fields.DurationField):
    widget = widgets.TextInput


class RegexField(fields.RegexField):
    widget = widgets.TextInput


class EmailField(fields.EmailField):
    widget = widgets.EmailInput


class FileField(fields.FileField):
    widget = widgets.ClearableFileInput


class ImageField(fields.ImageField):
    widget = widgets.ClearableFileInput


class URLField(CharField):
    widget = widgets.URLInput


class BooleanField(Field):
    widget = widgets.CheckboxInput


class NullBooleanField(BooleanField):
    widget = widgets.Select


class ChoiceField(fields.ChoiceField):
    widget = widgets.Select


class TypedChoiceField(fields.TypedChoiceField):
    widget = widgets.Select


class MultipleChoiceField(fields.MultipleChoiceField):
    widget = widgets.SelectMultiple


class TypedMultipleChoiceField(fields.TypedMultipleChoiceField):
    widget = widgets.SelectMultiple


class ComboField(fields.ComboField):
    widget = widgets.TextInput


class MultiValueField(fields.MultiValueField):
    widget = widgets.TextInput
    

class FilePathField(fields.FilePathField):
    widget = widgets.Select


class SplitDateTimeField(fields.SplitDateTimeField):
    widget = widgets.TextInput


class GenericIPAddressField(fields.GenericIPAddressField):
    widget = widgets.TextInput


class SlugField(fields.SlugField):
    widget = widgets.TextInput


class UUIDField(fields.UUIDField):
    widget = widgets.TextInput


class JSONField(fields.JSONField):
    widget = widgets.TextInput
