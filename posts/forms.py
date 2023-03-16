from django import forms

from .models import Comments_Model



class CommentsForm(forms.ModelForm):
    # comment_text = forms.CharField()
    class Meta:
        model = Comments_Model
        fields = ['comment_text']

        
class PollForm(forms.Form):
    prefix = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'prefix', 'placeholder': 'Insert Prefix', 'list': 'prefix-choices'}))
    question = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'question', 'placeholder': 'Insert Question'}))
    # 'number_options': forms.Select(attrs={'required': True}),
    choice1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'choice1', 'placeholder': 'Insert Option 1'}))
    choice2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'choice2', 'placeholder': 'Insert Choice 2'}))
    # 'choice3': forms.TextInput(attrs={'placeholder': 'Insert Option 3'}),
    # 'choice4': forms.TextInput(attrs={'placeholder': 'Insert Option 4'}),
    delay = forms.ChoiceField(choices=[('no-delay', 'No delay'), ('8-hours', '8 hours'), ('24-hours', '24 hours')], widget=forms.RadioSelect(attrs={'class': 'radio'}))
    categories = forms.MultipleChoiceField(choices=[('sports', 'Sports'), ('entertainment', 'Entertainment')], widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}), required=False)
	
