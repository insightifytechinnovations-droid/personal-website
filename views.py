from django.shortcuts import render, redirect
from .models import ClientRequest
from .chatbot_engine import insightify_ai_bot # Aapka AI engine import kiya

def submit_form(request):
    if request.method == 'POST':
        # Form se data uthana (HTML fields ke exact naam ke anusaar)
        name = request.POST.get('Name')
        mobile = request.POST.get('Phone')
        email = request.POST.get('email')
        url = request.POST.get('Website_URL')
        reqs = request.POST.get('Requirements')

        # Database mein save karna
        new_client = ClientRequest.objects.create(
            full_name=name,
            mobile_number=mobile,
            email_id=email,
            client_website_url=url,
            requirements=reqs
        )

        # AI ko trigger karna (Audit shuru karne ke liye)
        audit_report = insightify_ai_bot(f"Audit this website: {url} with requirements: {reqs}", language="hi")
        
        # Report update karna
        new_client.status = "Audit Complete"
        new_client.save()

        return render(request, 'thank_you.html', {'report': audit_report})

    return render(request, 'contact_form.html')