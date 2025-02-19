from django.db import models
from registros.models import Usuario
import random
import string
from django.utils.timezone import now, timedelta
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_short_code():
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not ShortenedURL.objects.filter(short_code=short_code).exists():
            return short_code

class ShortenedURL(models.Model):
    # Função para definir a data de expiração (2 minutos a partir da criação)
    def get_expiration_date():
        return now() + timedelta(minutes=2)

    original_url = models.URLField()  # URL original
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    user = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True) 
    expires_at = models.DateTimeField(default=get_expiration_date)  

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    # Verifica se o link expirou
    def is_expired(self):
        return self.expires_at <= now()

class Click(models.Model):
    url = models.ForeignKey(ShortenedURL, on_delete=models.CASCADE, related_name="clicks") 
    user = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL)  
    ip_address = models.GenericIPAddressField(null=True, blank=True)  
    user_agent = models.TextField(null=True, blank=True)  
    clicked_at = models.DateTimeField(default=now)  
    def __str__(self):
        return f"Click on {self.url.short_code} at {self.clicked_at}"

class QRCode(models.Model):
    url = models.OneToOneField(ShortenedURL, on_delete=models.CASCADE, related_name="qr_code")  
    image = models.ImageField(upload_to="qrcodes/", blank=True, null=True) 

    
    def generate_qr_code(self):
        qr = qrcode.make(self.url.original_url)  
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        self.image.save(f"{self.url.short_code}.png", ContentFile(buffer.getvalue()), save=False)

    
    def save(self, *args, **kwargs):
        if not self.image:
            self.generate_qr_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"QR Code for {self.url.short_code}"

class Categoria(models.Model):
    nome = models.CharField(max_length=50, unique=True)  # Nome da categoria

    def __str__(self):
        return self.nome

class ShortenedURLCategoria(models.Model):
    url = models.ForeignKey("links.ShortenedURL", on_delete=models.CASCADE)  # Relacionamento com ShortenedURL
    categoria = models.ForeignKey("Categoria", on_delete=models.CASCADE)  # Relacionamento com Categoria

    class Meta:
        unique_together = ("url", "categoria")  # Garante que a combinação URL-Categoria seja única

    def __str__(self):
        return f"{self.url.short_code} - {self.categoria.nome}"