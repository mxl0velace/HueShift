from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['body_text','has_image','image_url']
        labels = {
            'body_text' : ''
        }
        widgets = {
            'body_text' : forms.Textarea(attrs={
                'rows' : 4,
                'cols' : 80,
                'maxlength' : Post._meta.get_field('body_text').max_length,
                'style':'resize:none;',
                'placeholder':'Piece text...'
            }),
            'image_url' : forms.TextInput(attrs={
                'placeholder':'https://i.imgur.com/[YOURCODE].[EXT]'
            })
        }
