from django import forms
from .models import File
import os

class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ('csv_file',)
        Widget = {'csv_file':forms.FileInput(attrs={'class': 'form-control'})}
    
    def clean(self):
        print('clean')
        file_path = "media/" + self.cleaned_data.get('csv_file').name
        if os.path.isfile(file_path):
            raise forms.ValidationError('File already exists! Rename and upload again') 
        return self.cleaned_data