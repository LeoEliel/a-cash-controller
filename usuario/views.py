from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CadastroForm


class CadastroView(CreateView):
    form_class = CadastroForm
    template_name = 'usuario/cadastro.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada, faça login.')
        return response
