from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

from django.core.exceptions import ValidationError

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file', help_text='max. 42 megabytes', required=False, validators=[file_size])

def file_size(value): # add this to some file where you can import it from
    limit = 2 * 1024 * 1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 2 MiB.')

