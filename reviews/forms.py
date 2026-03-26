from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': 1,
            'max': 5,
        }),
    )

    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Share your thoughts...',
                'rows': 5,
            }),
        }
