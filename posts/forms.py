from django import forms

from .models import Comments_Model



class CommentsForm(forms.ModelForm):
    # comment_text = forms.CharField()
    class Meta:
        model = Comments_Model
        fields = ['comment_text']

from django import forms
from .models import Post_Model, Options_Model

from django import forms
from django.utils import timezone
from .models import Post_Model, Options_Model

class PollForm(forms.ModelForm):
    PREFIX_OPTIONS = [
        ('Show of hands if', 'Show of hands if'),
        ('Would you rather', 'Would you rather'),
        ('Do you prefer', 'Do you prefer'),
        ('Have you ever', 'Have you ever'),
        ('How important is', 'How important is'),
        ('own_ques', 'Type your own question ...')
    ]
    prefix = forms.ChoiceField(choices=PREFIX_OPTIONS)
    question = forms.CharField(max_length=300)
    DELAY_CHOICES = [
        ('0', 'No Delay'),
        ('8', '8 Hours'),
        ('24', '24 Hours'),
    ]
    delay = forms.ChoiceField(choices=DELAY_CHOICES)
    category = forms.MultipleChoiceField(choices=Post_Model.category_list)

    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)
    choice3 = forms.CharField(max_length=200, required=False)
    choice4 = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Post_Model
        fields = ['prefix',  'category']

    # def save(self, commit=True):
    #     post = super().save(commit=False)
    #     post.question_text = self.cleaned_data['prefix'] + ' ' + self.cleaned_data['question']
    #     delay = int(self.cleaned_data['delay'])
    #     post.created_time = timezone.now()
    #     post.result_reveal_time = post.created_time + timezone.timedelta(hours=delay)
    #     post.category = self.cleaned_data['category']

    #     if commit:
    #         post.save()

    #     choice1 = Options_Model(
    #         question=post,
    #         choice_text=self.cleaned_data['choice1'],
    #     )
    #     choice2 = Options_Model(
    #         question=post,
    #         choice_text=self.cleaned_data['choice2'],
    #     )
    #     if self.cleaned_data['choice3']:
    #         choice3 = Options_Model(
    #             question=post,
    #             choice_text=self.cleaned_data['choice3'],
    #         )
    #     if self.cleaned_data['choice4']:
    #         choice4 = Options_Model(
    #             question=post,
    #             choice_text=self.cleaned_data['choice4'],
    #         )
        
    #     for choice in [choice1, choice2, choice3, choice4]:
    #         if choice:
    #             choice.save()

    #     return post


# class PollForm(forms.Form):
#     prefix = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'prefix', 'placeholder': 'Insert Prefix', 'list': 'prefix-choices'}))
#     question = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'question', 'placeholder': 'Insert Question'}))
#     # 'number_options': forms.Select(attrs={'required': True}),
#     choice1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'choice1', 'placeholder': 'Insert Option 1'}))
#     choice2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'id': 'choice2', 'placeholder': 'Insert Choice 2'}))
#     # 'choice3': forms.TextInput(attrs={'placeholder': 'Insert Option 3'}),
#     # 'choice4': forms.TextInput(attrs={'placeholder': 'Insert Option 4'}),
#     delay = forms.ChoiceField(choices=[('no-delay', 'No delay'), ('8-hours', '8 hours'), ('24-hours', '24 hours')], widget=forms.RadioSelect(attrs={'class': 'radio'}))
#     categories = forms.MultipleChoiceField(choices=[('sports', 'Sports'), ('entertainment', 'Entertainment')], widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox'}), required=False)
	
