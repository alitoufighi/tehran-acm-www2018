from ckeditor.widgets import CKEditorWidget
from django import forms

from blog.models import Post, Tag


class NewCommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, max_length=1000, label='متن نظر')


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['tags', 'author']


class AddTagToPostForm(forms.Form):
    tag = forms.ModelChoiceField(label='تگ', queryset=Tag.objects.all())
