from django.contrib import admin
from django.urls import path
from zapp.views import create_document, list_documents, update_document, delete_document, get_document_by_id



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/documents/', create_document, name='create_document'),
    path('api/get-documents/', list_documents, name='list_documents'),
    path('api/update-docs/<int:id>/', update_document, name='update_document'),
    path('api/delete-doc/<int:id>/', delete_document, name='delete-document'),
    path('api/get-documents-by-id/<int:id>/', get_document_by_id, name='get_document_by_id'),
]
