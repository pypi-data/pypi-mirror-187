from django.forms import formsets
from .fields import BooleanField, IntegerField
from .widgets import HiddenInput
from .forms import Form

class ManagementForm(Form):
    TOTAL_FORMS = IntegerField(widget=HiddenInput)
    INITIAL_FORMS = IntegerField(widget=HiddenInput)
    MIN_NUM_FORMS = IntegerField(required=False, widget=HiddenInput)
    MAX_NUM_FORMS = IntegerField(required=False, widget=HiddenInput)
