from io import BytesIO

from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


class UsuarioQuerysetMixin:
    def get_queryset(self):
        return super().get_queryset().filter(usuario=self.request.user)

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class GeraPDFMixin:
    pdf_template_name = None

    def render_to_pdf(self, template, context):
        html = get_template(template).render(context)
        buffer = BytesIO()
        pisa.CreatePDF(html, dest=buffer)
        return HttpResponse(buffer.getvalue(), content_type='application/pdf')
