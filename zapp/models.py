from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    api_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)


class Document(models.Model):
    open_id = models.IntegerField()
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

class Signer(models.Model):
    token = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    status = models.CharField(max_length=50)
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
