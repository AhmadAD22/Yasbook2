from django.db import models
import os

class Category(models.Model):
    name = models.CharField(max_length=50)
    en_name=models.CharField(max_length=255, verbose_name='اسم التصنيف بالإنكليزية')
    image = models.ImageField(upload_to='media/category/',null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True,null=True)
    

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        super(Category, self).delete(*args, **kwargs)


class MainService(models.Model):
    category = models.ForeignKey(Category,verbose_name='القسم التابع له',  on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name='اسم الخدمة')
    en_name=models.CharField(max_length=255, verbose_name='اسم الخدمة بالإنكليزية')
    image = models.ImageField(upload_to='media/service/',null=True, verbose_name='رفع الصورة')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء',blank=True,null=True)
    updated_on = models.DateTimeField(auto_now=True, verbose_name='تاريخ التحديث',blank=True,null=True)
    

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        # Delete the associated image file
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        
        super(MainService, self).delete(*args, **kwargs)