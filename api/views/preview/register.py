"""
    Preview uploading
"""

from django import forms
from hackfsu_com.views.generic import ApiView
from django.http.request import HttpRequest
from django.core.exceptions import ValidationError
from hackfsu_com.util import acl
from api.models import PreviewEmail, Hackathon

EMAIL = 'email'
INTEREST = 'interest'

class RequestForm(forms.Form):
    email = forms.CharField(max_length=100)
    interest = forms.CharField(max_length=100)

class RegisterView(ApiView):
    request_form_class = RequestForm

    def work(self, request: HttpRequest, req: dict, res: dict):
        # Clean fields
        req[EMAIL] = req[EMAIL].lower()
        req[INTEREST] = req[INTEREST].lower()

        # Make sure interest is okay
        if req[INTEREST] not in ['volunteer', 'hacker', 'sponsor']:
            raise ValidationError('Not a valid interest.', params=[INTEREST])

        if PreviewEmail.objects.filter(email=req[EMAIL], interest=req[INTEREST]).exists():
            raise ValidationError('Email already submitted for that role.', params=[EMAIL])

        # TODO: at the time of writing this, we had not yet updated
        # the current hackathon value, meaning that this is being written
        # for HackFSU 2018, but when this was being used the value was getting
        # HackFSU 2017. Update the data when you fix this.
        current_hackathon = Hackathon.objects.current()

        # Attempt to save the user
        PreviewEmail(
            hackathon=current_hackathon,
            email=req[EMAIL],
            interest=req[INTEREST]
        ).save()
