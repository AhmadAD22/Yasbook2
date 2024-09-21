from django.shortcuts import render
from provider_details.models import Store
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework import status

# Create your views here.
def home (request):
    
    return render(request,'homew.html')

def yasbook_page (request):
    stores=Store.objects.all()
    context={
        'stores':stores,
    }
    
    return render(request,'yasbook.html',context)

def about (request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def terms(request):
    terms=Term.objects.all()
    return render(request,'terms.html',{"terms":terms})

def privacy(request):
    privacy=Privacy.objects.all()
    return render(request,'privacy.html',{"privacy":privacy})




class SubmitFormView(APIView):
    permission_classes = []
    authentication_classes=[]
    def post(self, request):
        name = request.data.get('name')
        subject = request.data.get('subject')
        email = request.data.get('email')
        message = request.data.get('message')

        # Perform any necessary validation or processing

        # Send email notification
        email_subject = f'New contact form submission: {subject}'
        email_body = f'Name: {name}\nEmail: {email}\n\n{message}'
        
        try:
            send_mail(email_subject, email_body,"", ["yasafco@gmail.com"], fail_silently=False)
            
            return Response({'success': 'Email sent'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)