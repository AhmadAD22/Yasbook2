from django.db import models

# Create your models here.
class FavorateProduct(models.Model):
    product=models.ForeignKey("provider_details.Product", on_delete=models.CASCADE)
    customer=models.ForeignKey("auth_login.customer", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('product', 'customer')
    
    
class FavorateService(models.Model):
    service=models.ForeignKey("provider_details.Service", on_delete=models.CASCADE)
    customer=models.ForeignKey("auth_login.customer", on_delete=models.CASCADE)
    class Meta:
        unique_together = ('service', 'customer')