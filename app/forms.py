from django import forms
from app.models import RequestLog


class RequestLogForm(forms.ModelForm):
    class Meta:
        model = RequestLog
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Текст обращения'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['operator'].label_from_instance = lambda obj: f"{obj.fio} ({obj.operator_id or '-'})"

        self.fields['service_id'].required = False
        self.fields['num_app'].required = False

        self.fields['phone_num'].widget.attrs['placeholder'] = 'обязательное поле'
        self.fields['theme'].widget.attrs['placeholder'] = 'обязательное поле'
        self.fields['operator'].widget.attrs['placeholder'] = 'обязательное поле'

        self.fields['num_app'].widget.attrs['placeholder'] = 'необязательное поле'
        self.fields['service_id'].widget.attrs['placeholder'] = 'необязательное поле'
        self.fields['comment'].widget.attrs['placeholder'] = 'Текст обращения'
