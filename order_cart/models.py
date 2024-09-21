from django.db import models
from provider_details.models import *
from auth_login.models import *
import decimal
from decimal import Decimal, ROUND_HALF_UP
from decimal import Decimal, InvalidOperation
from utils.qr_code import *
from dashboard.models import Config
class Status(models.TextChoices):
    UNCHECKED = 'UNCHECKED','Unchecked'
    PENDING = 'PENDING','Pending'
    IN_PROGRESS = 'IN_PROGRESS','In Progress'
    COMPLETED = 'COMPLETED','Completed'
    CANCELLED = 'CANCELLED','Cancelled'
    REJECTED='REJECTED','Rejected'   

class Cart(models.Model):
    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    @property
    def total_price(self):
        product_items = self.cartitem_set.all()
        service_items = self.servicecartitem_set.all()

        product_total = sum(item.product.price * item.quantity for item in product_items)
        service_total = sum(item.service.price * item.quantity for item in service_items)

        return product_total + service_total
    def __str__(self):   
        return self.customer.name

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class ServiceCartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    specialist = models.ForeignKey(StoreSpecialist, on_delete=models.CASCADE, null=True)
    time_start = models.TimeField(verbose_name='وقت البدء', null=True)
    date = models.DateTimeField(verbose_name='تاريخ الحجز', blank=True, null=True)
    duration= models.PositiveIntegerField(verbose_name='مدة الخدمة (بالدقائق)', blank=True, null=True)


    class Meta:
        verbose_name = 'Service Cart Item'
        verbose_name_plural = 'Service Cart Items'


class ProductOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices)
    collected = models.BooleanField(default=False, verbose_name='تم تحصيلها', null=True, blank=True)
    date= models.DateTimeField(auto_now_add=True, verbose_name='تاريخ الإنشاء',blank=True,null=True)
    coupon=models.ForeignKey(Coupon, on_delete=models.SET_NULL,null=True,blank=True)
    qr_code = models.ImageField(upload_to="media/order/qr_code", null=True, blank=True)
    def total_price(self):
        return self.quantity * self.product.price_after_offer
    
    def tax(self):
        price=self.total_price() 
        price=Decimal(price)
        tax_config=Config.objects.first().tax
        return price * (decimal.Decimal(tax_config) / 100) if tax_config else decimal.Decimal(0)
    
    def price_with_tax(self):
        price=self.total_price() 
        price=Decimal(price)
        tax_config=Config.objects.first().tax
        tax =price * (decimal.Decimal(tax_config) / 100) if tax_config else decimal.Decimal(0)
       
        return round(tax  +price,2)
    
    def price_with_coupon(self):
        price = self.price_with_tax()
        if self.coupon:
            coupon_percent = decimal.Decimal(self.coupon.value) / 100
            price = price - (price * coupon_percent)
        return round(price, 2)





    def __str__(self):   
        return self.product.name
    


class ServiceOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    specialist = models.ForeignKey(StoreSpecialist, on_delete=models.CASCADE, null=True)
    time_start = models.TimeField(verbose_name='وقت البدء', null=True)
    date = models.DateTimeField(verbose_name='تاريخ الحجز', blank=True, null=True)
    duration = models.PositiveIntegerField(verbose_name='مدة الخدمة (بالدقائق)', blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices)
    collected = models.BooleanField(default=False, verbose_name='تم تحصيلها', null=True, blank=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    qr_code = models.ImageField(upload_to="media/order/qr_code", null=True, blank=True)

    @property
    def price(self):
        return decimal.Decimal(self.service.price_after_offer)
    
    def tax(self):
        price=self.price 
        tax_config=Config.objects.first().tax
        return price * (decimal.Decimal(tax_config) / 100) if tax_config else decimal.Decimal(0)
    
    def price_with_tax(self):
        price=self.price
        tax_config=Config.objects.first().tax
        tax =price * (decimal.Decimal(tax_config) / 100) if tax_config else decimal.Decimal(0)
       
        return round(tax  +price,2)
        
    def price_with_coupon(self):
        price = self.price_with_tax()
        price = Decimal(price)
        if self.coupon:
            coupon_percent = Decimal(self.coupon.value) / 100
            price = price - (price * coupon_percent)
            return price
        return price

    def __str__(self):   
        return self.service.name