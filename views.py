from django.shortcuts import render, redirect
from .models import ClientRequest
from .chatbot_engine import insightify_ai_bot 

def submit_form(request):
    if request.method == 'POST':
        # HTML form ke exact name attributes ke anusaar data uthana
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        url = request.POST.get('url')
        reqs = request.POST.get('requirements')

        # Database mein save karna
        new_client = ClientRequest.objects.create(
            full_name=name,
            mobile_number=mobile,
            email_id=email,
            client_website_url=url,
            requirements=reqs
        )

        # AI ko trigger karna (Audit shuru karne ke liye)
        audit_report = insightify_ai_bot(f"Audit this website: {url} with requirements: {reqs}")
        
        # Report update karna
        new_client.status = "Audit Complete"
        new_client.save()

        return render(request, 'thank_you.html', {'report': audit_report})

    return render(request, 'contact_form.html')