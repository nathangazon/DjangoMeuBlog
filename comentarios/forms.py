import requests
from django.forms import ModelForm

from .models import Comentario


class FormComentario(ModelForm):

    def clean(self):
        raw_data = self.data
        recaptcha_response = raw_data.get('g-recaptcha-response')

        recaptcha_request = requests.post(
            'https://www.google.com/recaptcha/api/siteverify',
            data={
                'secret': '6Lf0KmQkAAAAADU9vLprd6X1NbMztb7ys3v1RDQk',
                'response': recaptcha_response
            }
        )
        recaptcha_result = recaptcha_request.json()
        if not recaptcha_result.get('success'):
            self.add_error(
                'nome_comentario',
                'Desculpe Mr Robot, ocorreu um erro.'
            )

        print(recaptcha_result)

        cleaned_data = self.cleaned_data
        nome = cleaned_data.get('nome_comentario')
        comentario = cleaned_data.get('comentario')

        if len(nome) < 5:
            self.add_error(
                'nome_comentario',
                'Nome precisa ter mais de 5 caracteres.'
            )

    class Meta:
        model = Comentario
        fields = ('nome_comentario', 'email_comentario', 'comentario')
