<<<<<<< HEAD
from django.db import models

class ClientRequest(models.Model):
    # Client ki basic details
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()
    client_website_url = models.URLField()
    
    # Client ki requirements
    requirements = models.TextField()
    
    # Status tracking (AI apne aap manage karega)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment status
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
=======
from django.db import models

class ClientRequest(models.Model):
    # Client ki basic details
    full_name = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=15)
    email_id = models.EmailField()
    client_website_url = models.URLField()
    
    # Client ki requirements
    requirements = models.TextField()
    
    # Status tracking (AI apne aap manage karega)
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Payment status
    is_paid = models.BooleanField(default=False)
    
    def __str__(self):
>>>>>>> e7d22e130d6358a4a41f5e48260c9ad0975bc3f9
        return f"{self.full_name} - {self.client_website_url}"