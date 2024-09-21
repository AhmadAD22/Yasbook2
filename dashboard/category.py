from django import forms
from categroy.models import *
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required




class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name','en_name','image']
        labels = {
            'name': 'اسم التصنيف',
            'image': 'رفع الصورة',
        }
        labels = {
            'image': 'حمل صورة',
            'name': 'إسم التصنيف',
        }
        widgets = {
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
        
class MainServiceForm(forms.ModelForm):
    class Meta:
        model = MainService
        fields = ['category','en_name', 'name', 'image']
        labels = {
            'category': 'القسم التابع له',
            'name': 'اسم الخدمة',
            'image': 'رفع الصورة',
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'en_name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file', 'accept': 'image/*'}),
        }


@staff_member_required(login_url='login')
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, 'category/create_category.html', {'form': form})

@staff_member_required(login_url='login')
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

@staff_member_required(login_url='login')
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'category/update_category.html', {'form': form})

@staff_member_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')
    
    
###############Main Service####

@staff_member_required(login_url='login')
def create_main_service(request):
    if request.method == 'POST':
        form = MainServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('main_service_list')
    else:
        form = MainServiceForm()
    
    return render(request, 'category/main_service/create_main_service.html', {'form': form})

@staff_member_required(login_url='login')
def main_service_list(request):
    main_services = MainService.objects.all()
    return render(request, 'category/main_service/main_service_list.html', {'main_services': main_services})

@staff_member_required(login_url='login')
def update_main_service(request, main_service_id):
    main_service = MainService.objects.get(id=main_service_id)
    
    if request.method == 'POST':
        form = MainServiceForm(request.POST, request.FILES, instance=main_service)
        if form.is_valid():
            form.save()
            return redirect('main_service_list')
    else:
        form = MainServiceForm(instance=main_service)
    
    return render(request, 'category/main_service/update_main_service.html', {'form': form})

@staff_member_required(login_url='login')
def delete_main_service(request, main_service_id):
    main_service = MainService.objects.get(id=main_service_id)
    main_service.delete()
    return redirect('main_service_list')
    
  