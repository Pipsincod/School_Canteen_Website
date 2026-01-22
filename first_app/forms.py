from django import forms

class CommentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label="Comment", max_length=20)

class ClickerForm(forms.Form):
    hp = forms.IntegerField(label="HP", max_value=100, min_value=10, initial=0, widget=forms.NumberInput(attrs={
        'id': 'id_hp',
        'readonly': 'readonly',
    }))
    iq = forms.IntegerField(label="HP", max_value=100, min_value=10, initial=0, widget=forms.NumberInput(attrs={
        'id': 'id_iq',
        'readonly': 'readonly',
    }))
    happi_index = forms.IntegerField(label="HP", max_value=100, min_value=10, initial=0, widget=forms.NumberInput(attrs={
        'id': 'id_happi_index',
        'readonly': 'readonly',
    }))
