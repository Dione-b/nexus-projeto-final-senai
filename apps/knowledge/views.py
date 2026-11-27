"""Views do app knowledge (base de conhecimento) — US10.

Todas as views exigem o papel ``administrador`` (RN01).
"""

from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.accounts.permissions import administrador_required

from .forms import DocumentUploadForm
from .models import Document


@administrador_required
def document_list(request):
    """Lista os documentos da base de conhecimento e exibe o formulário."""
    contexto = {
        "documentos": Document.objects.select_related("enviado_por").all(),
        "form": DocumentUploadForm(),
    }
    return render(request, "knowledge/document_list.html", contexto)


@administrador_required
@require_POST
def document_upload(request):
    """Recebe o upload (HTMX ou POST tradicional) e cria o documento."""
    form = DocumentUploadForm(request.POST, request.FILES)

    if not form.is_valid():
        # Resposta parcial para o HTMX: apenas a mensagem de erro, sem trace.
        return render(
            request,
            "knowledge/partials/document_form.html",
            {"form": form},
        )

    try:
        documento = form.save(commit=False)
        documento.enviado_por = request.user
        documento.save()
    except (IntegrityError, OSError):
        # Falha de armazenamento/gravação: mensagem segura, sem expor detalhes.
        form.add_error(None, "Não foi possível gravar o arquivo. Tente novamente.")
        return render(
            request,
            "knowledge/partials/document_form.html",
            {"form": form},
        )

    messages.success(request, f'Documento "{documento.titulo}" enviado com status pendente.')

    if request.headers.get("HX-Request"):
        # HTMX: instrui o navegador a recarregar a página com o novo documento.
        resposta = HttpResponse(status=200)
        resposta["HX-Redirect"] = reverse("knowledge:document_list")
        return resposta

    return redirect("knowledge:document_list")
