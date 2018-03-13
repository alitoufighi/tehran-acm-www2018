import re
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from account.models import StudentField
from account.validators import validate_student_id, email_validator, password_validator
from blog.models import Tag


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label=_('email'), max_length=200, required=True,
                             validators=[email_validator])
    field = forms.ModelChoiceField(label=_('field'), queryset=StudentField.objects.all(), required=True)
    student_id = forms.IntegerField(label=_('student id'), validators=[validate_student_id], required=True)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        validators=[password_validator]
    )

    def clean(self):
        super(UserCreationForm, self).clean()
        email = ''
        if 'email' in self.cleaned_data:
            email = self.cleaned_data['email']
        username = self.cleaned_data['username']
        if User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Invalid data.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'field', 'student_id')
