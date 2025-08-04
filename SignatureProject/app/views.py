from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
import os
import tempfile
from .signature_utils import read_text_file, sign_document, save_signature, verify_signature

# Create your views here.

def sign_document_view(request):
    """
    View for displaying and signing text documents
    """
    context = {}
    
    if request.method == 'POST':
        username = request.POST.get('username')
        document_file = request.FILES.get('document')
        
        # Validate inputs
        if not username:
            messages.error(request, "Veuillez entrer un nom d'utilisateur")
            return render(request, 'app/sign_document.html', context)
            
        if not document_file:
            messages.error(request, "Veuillez sélectionner un fichier")
            return render(request, 'app/sign_document.html', context)
            
        # Check file extension
        if not document_file.name.endswith('.txt'):
            messages.error(request, "Seuls les fichiers .txt sont acceptés")
            return render(request, 'app/sign_document.html', context)
        
        try:
            # Read document content
            document_content = read_text_file(document_file)
            
            # Sign the document
            signature, timestamp = sign_document(document_content, username)
            
            # Save the signature
            signature_file = save_signature(signature, timestamp, document_file.name, username)
            
            # Add success message
            messages.success(request, f"Document signé avec succès! Signature sauvegardée dans {signature_file}")
            
            # Update context with document content and signature info
            context.update({
                'username': username,
                'document_content': document_content,
                'document_name': document_file.name,
                'signature_file': signature_file,
                'timestamp': timestamp,
            })
            
        except FileNotFoundError as e:
            messages.error(request, f"Erreur: {str(e)}")
        except Exception as e:
            messages.error(request, f"Une erreur s'est produite lors de la signature: {str(e)}")
    
    return render(request, 'app/sign_document.html', context)

def view_signature(request, signature_file):
    """
    View for displaying a signature file
    """
    try:
        with open(signature_file, 'rb') as f:
            signature_content = f.read().decode('utf-8', errors='replace')
        
        return render(request, 'app/view_signature.html', {
            'signature_content': signature_content,
            'signature_file': signature_file
        })
    except Exception as e:
        messages.error(request, f"Erreur lors de l'affichage de la signature: {str(e)}")
        return redirect('sign_document')

def verify_signature_view(request):
    """
    View for verifying document signatures
    """
    result = None
    original_content = None
    
    if request.method == 'POST':
        if 'username' in request.POST and 'document' in request.FILES and 'signature' in request.FILES:
            username = request.POST['username']
            document = request.FILES['document']
            signature_file = request.FILES['signature']
            
            # Check file extension for document
            if not document.name.endswith('.txt'):
                messages.error(request, "Only .txt files are supported for documents")
                return render(request, 'app/verify_signature.html')
                
            # Check file extension for signature
            if not signature_file.name.endswith('.sig'):
                messages.error(request, "Only .sig files are supported for signatures")
                return render(request, 'app/verify_signature.html')
            
            # Save uploaded files temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as doc_temp:
                for chunk in document.chunks():
                    doc_temp.write(chunk)
                doc_path = doc_temp.name
                
            with tempfile.NamedTemporaryFile(delete=False, suffix='.sig') as sig_temp:
                for chunk in signature_file.chunks():
                    sig_temp.write(chunk)
                sig_path = sig_temp.name
            
            try:
                # Read document content for display
                with open(doc_path, 'r', encoding='utf-8') as f:
                    original_content = f.read()
                
                # Verify signature
                result = verify_signature(username, doc_path, sig_path)
                
                if result:
                    messages.success(request, "Signature is valid! Document integrity verified.")
                else:
                    messages.error(request, "Invalid signature. The document may have been tampered with or signed by someone else.")
                    
            except Exception as e:
                messages.error(request, f"Error verifying signature: {e}")
            finally:
                # Clean up temporary files
                os.unlink(doc_path)
                os.unlink(sig_path)
        else:
            messages.error(request, "Please provide username, document, and signature file")
    
    return render(request, 'app/verify_signature.html', {
        'result': result,
        'content': original_content
    })
