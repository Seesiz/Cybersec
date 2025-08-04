from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .utils import register_user
import os

# Create your views here.

def signup_view(request):
    """View for user registration with public key"""
    if request.method == 'POST':
        username = request.POST.get('username')
        public_key_file = request.FILES.get('public_key')
        
        # Validate inputs
        if not username:
            messages.error(request, "Le nom d'utilisateur est requis.")
            return render(request, 'sign_up/signup.html')
            
        if not public_key_file:
            messages.error(request, "Le fichier de clé publique est requis.")
            return render(request, 'sign_up/signup.html')
        
        # Read the public key file
        try:
            public_key_content = public_key_file.read().decode('utf-8')
            
            # Register the user
            success = register_user(username, public_key_content)
            
            if success:
                messages.success(request, f"Utilisateur {username} enregistré avec succès!")
                return redirect('signup_success')
            else:
                messages.error(request, "Erreur lors de l'enregistrement. Vérifiez que l'utilisateur n'existe pas déjà.")
                return render(request, 'sign_up/signup.html')
                
        except Exception as e:
            messages.error(request, f"Erreur lors de la lecture du fichier: {str(e)}")
            return render(request, 'sign_up/signup.html')
    
    # GET request - show the form
    return render(request, 'sign_up/signup.html')

def signup_success_view(request):
    """Success page after registration"""
    return render(request, 'sign_up/success.html')
