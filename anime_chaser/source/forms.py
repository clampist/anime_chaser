from django import forms

from .models import Source

import mistune


class SourceForm(forms.ModelForm):
    nickname = forms.CharField(
        label='昵称',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    email = forms.CharField(
        label='Email',
        max_length=50,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    website = forms.CharField(
        label='网站',
        max_length=100,
        widget=forms.widgets.Input(
            attrs={'class': 'form-control', 'style': "width: 60%;"}
        )
    )
    content = forms.CharField(
        label='内容',
        max_length=500,
        widget=forms.widgets.Input(
            attrs={'rows': 6, 'cols': 60, 'class': 'form-control'}
        )
    )

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError('内容的长度太短！')
        content = mistune.markdown(content)
        return content

    class Meta:
        model = Source
        fields = ['nickname', 'email', 'website', 'content']
