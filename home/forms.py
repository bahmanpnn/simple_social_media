from django import forms
from .models import Post,PostComment


class CreateUpdatePostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','body']

        widgets={
            'body':forms.Textarea(attrs={
                'class':'form-control bg-light',
                'rows':5,
            }),
            'title':forms.TextInput(attrs={
                'class':'form-control bg-light'
            })
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model=PostComment
        fields=('body',)

        widgets={
            'body':forms.Textarea(attrs={
                'class':'form-control bg-light',
                'rows':2,
            })
        }

class ReplyCommentForm(forms.ModelForm):
    class Meta:
        model=PostComment
        fields=('body',)

        widgets={
            'body':forms.Textarea(attrs={
                'class':'form-control bg-light',
                'rows':2,
            })
        }


class PostSearchForm(forms.Form):

    search=forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control col-md-3',
        'placeholder':'search'
    }))
