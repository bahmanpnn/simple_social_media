from django.forms import ModelForm
from .models import Post


class CreateUpdatePostForm(ModelForm):
    class Meta:
        model=Post
        fields=['title','body']

        # widgets={
        #     'title':CharField(attrs={
        #         'class':'col-md-3'
        #     }),
        #     'body':TextInput(attrs={
        #         'class':'col-md-3',
        #         'rows':6,
        #         'cols':12
        #     })
        # }

