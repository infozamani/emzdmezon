# # در apps/comment_scoring_favorites/forms.py
# from django import forms

# class CommentForm(forms.Form):
#     product_id = forms.CharField(
#         widget=forms.HiddenInput(),
#         required=False
#     )
#     comment_id = forms.CharField(
#         widget=forms.HiddenInput(),
#         required=False
#     )
#     comment_text = forms.CharField(
#         label="",
#         error_messages={'required': 'لطفاً متن نظر را وارد کنید.'},
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'placeholder': 'متن نظر خود را اینجا بنویسید...',
#             'rows': 4,
#             'style': 'resize: vertical; min-height: 100px;'
#         }),
#         min_length=10,
#         max_length=500
#     )
    
#     def clean_comment_text(self):
#         comment_text = self.cleaned_data.get('comment_text', '').strip()
#         if len(comment_text) < 10:
#             raise forms.ValidationError('متن نظر باید حداقل 10 کاراکتر باشد.')
#         return comment_text
from django import forms
#----------------------------------------------------------------
## create a form for comment
class CommentForm(forms.Form):
    product_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    comment_id = forms.CharField(widget = forms.HiddenInput(), required = False)
    comment_text = forms.CharField(label="",
                                  error_messages={'required':'این فیلد نمی تواند خالی باشد'}, 
                                  widget = forms.Textarea(attrs={'class': 'form-control', 'placeholder' : 'متن نظر', 'rows':4}))