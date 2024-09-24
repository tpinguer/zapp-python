import requests
import json
from django.shortcuts import render
from django.http import JsonResponse
from .models import Document, Signer, Company
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_document(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            company = Company.objects.first()

            if not company:
                return JsonResponse({'error': 'Company não encontrada'}, status=400)

            headers = {
                'Authorization': f'Bearer {company.api_token}',
                'Content-Type': 'application/json'
            }

            payload = {
                'name': data['name'],
                'url_pdf': data['url_pdf'],
                'signers': [{'name': signer['name'], 'email': signer['email']} for signer in data['signers']]
            }

            response = requests.post(
                "https://sandbox.api.zapsign.com.br/api/v1/docs/",
                json=payload, headers=headers
            )

            print(f"Status da resposta: {response.status_code}")
            print(f"Resposta da API: {response.text}")
            if response.status_code == 200:
                try:
                    result = response.json()
                    print(f"Resultado da API: {result}")  
                    document = Document.objects.create(
                        open_id=result['open_id'],
                        token=result['token'],
                        name=result['name'],
                        status=result['status'],
                        company=company
                    )

                    for signer in result['signers']:
                        Signer.objects.create(
                            token=signer['token'],
                            name=signer['name'],
                            email=signer.get('email', ''),
                            status=signer['status'],
                            document=document
                        )
                    return JsonResponse({'message': 'Documento criado com sucesso'}, status=201)
                except Exception as e:
                    print(f"Erro ao criar no banco de dados: {str(e)}")
                    return JsonResponse({'error': 'Erro ao criar no banco de dados', 'detalhe': str(e)}, status=500)

            return JsonResponse({'error': 'Erro ao criar documento', 'detalhe': response.text}, status=response.status_code)

        except Exception as e:
            return JsonResponse({'error': 'Erro inesperado', 'detalhe': str(e)}, status=500)

def list_documents(request):
    if request.method == 'GET':
        documentos = Document.objects.all().values()
        return JsonResponse(list(documentos), safe=False)

def get_document_by_id(request, id):
    if request.method == 'GET':
        documento = get_object_or_404(Document, id=id)
        return JsonResponse({
            'id': documento.id,
            'name': documento.name,
            'created_at': documento.created_at,
            'status': documento.status
        })

@csrf_exempt
def update_document(request, id):
    if request.method == 'PUT':
        try:
            document = Document.objects.get(id=id)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Documento não encontrado'}, status=404)
        
        data = json.loads(request.body)
        
        document.name = data.get('name', document.name)
        document.token = data.get('token', document.token)
        document.status = data.get('status', document.status)
        document.save()
        
        return JsonResponse({'message': 'Documento atualizado com sucesso'}, status=200)

@csrf_exempt
def delete_document(request, id):
    if request.method == 'DELETE':
        try:
            document = Document.objects.get(id=id)
        except Document.DoesNotExist:
            return JsonResponse({'error': 'Documento não encontrado'}, status=404)
        
        document.delete()
        
        return JsonResponse({'message': 'Documento deletado com sucesso'}, status=200)
