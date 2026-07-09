from django import forms
from .models import Note


class NoteForm(forms.ModelForm):

    class Meta:
        model = Note
        fields = [
            'note_cc',
            'note_examen'
        ]

        widgets = {
            'note_cc': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Note CC'
                }
            ),

            'note_examen': forms.NumberInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Note Examen'
                }
            ),
        }
