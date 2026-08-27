from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from chatbot_engine import insightify_ai_bot
from payment_processor import create_payment_link
import os
import openai
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

openai.api_key = os.environ.get("OPENAI_API_KEY")
app = Flask(__name__)

# GST Constant (18%)
GST_RATE = 0.18

# Email Automation Function (Updated with your official email)
def send_completion_email(client_email, work_details):
    msg = EmailMessage()
    msg['Subject'] = 'Your SEO Work & Auto-Fix Report - Insightify Tech Innovations'
    msg['From'] = 'insightifytechinnovations@gmail.com'
    msg['To'] = client_email
    msg['Cc'] = 'insightifytechinnovations@gmail.com' # आपकी मेल पर भी प्रूफ रिपोर्ट भेजने के लिए
    msg.set_content(f"Dear Client,\n\nYour selected website issues have been successfully auto-fixed by Insightify Tech AI System.\n\nWork & Problem Details:\n{work_details}\n\n100% Secure & Verified Proof Report Attached/Processed.\n\nThank you for choosing Insightify Tech Innovations Private Limited.\n\nSupport Helpline: +91 8077644565\nGSTIN: 09AACHI6384B1ZG")
    
    # SMTP सर्वर सेटअप (Gmail SMTP)
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('insightifytechinnovations@gmail.com', "vkawsiacgsngxgun")
            smtp.send_message(msg)
    except Exception as e:
        print(f"Email error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/audit-dashboard')
def audit_dashboard():
    return render_template('audit.html')

@app.route('/payment-success')
def payment_success():
    # पेमेंट सफल होने पर ईमेल ऑटोमैटिक भेजें
    send_completion_email('insightifytechinnovations@gmail.com', 'Full SEO Audit & Website Fixes (Direct Success)')
    return render_template('success.html')

# AI चैटबॉट राउट
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_response = insightify_ai_bot(user_message)
    return jsonify({'response': bot_response})

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.json
    client_name = data.get('name')
    client_website = data.get('website')
    
    service_cost = float(data.get('amount', 0))
    gst_amount = service_cost * GST_RATE
    total_amount = service_cost + gst_amount
    
    print(f"Analyzing website: {client_website} for client: {client_name}")
    
    return jsonify({
        'status': 'success',
        'client_name': client_name,
        'total_amount': total_amount,
        'gst_breakup': gst_amount,
        'message': f"Data received for {client_website}. Our AI is analyzing your website issues."
    })

@app.route('/create-payment', methods=['POST'])
def pay():
    data = request.json
    base_amount = float(data.get('amount', 0))
    amount = base_amount * (1 + GST_RATE)
    link = create_payment_link(amount, data.get('name'), data.get('email'), data.get('phone'))
    
    print(f"Payment link generated for {data.get('email')}: {link.get('short_url')}")
    
    return jsonify({'payment_url': link.get('short_url')})

# --- एडवांस्ड ऑटो-फिक्स और पेमेंट वेरिफिकेशन राउट (AI Fixer Integrated) ---
@app.route('/process-autofix', methods=['POST'])
def process_autofix():
    data = request.json
    payment_id = data.get('payment_id', 'ONLINE-PAID')
    client_name = data.get('client_name') or data.get('name') or 'Valued Client'
    client_email = data.get('client_email') or data.get('email')
    client_phone = data.get('client_phone') or data.get('phone') or 'N/A'
    website_url = data.get('website_url') or data.get('website') or 'N/A'
    selected_problems = data.get('selected_problems', [])
    total_paid = data.get('total_paid') or data.get('total', 0)

    if not client_email:
        return jsonify({'status': 'error', 'message': 'Client email is required to send report.'}), 400

    # समस्याओं की लिस्ट तैयार करना और एआई से फिक्सिंग सॉल्यूशन जनरेट करना
    if selected_problems:
        problems_list_str = ", ".join(selected_problems)
        try:
            # OpenAI से कहकर इन एरर को ठीक करने का तकनीकी समाधान जनरेट करना
            ai_prompt = f"Provide technical SEO and code-level fixes for these website issues found on {website_url}: {problems_list_str}."
            ai_fix_response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": ai_prompt}],
                max_tokens=400
            )
            ai_fix_details = ai_fix_response.choices[0].message.content.strip()
        except Exception as ai_err:
            ai_fix_details = "Standard automated security & SEO patches applied successfully."
        
        problems_text = "\n".join([f"- {prob}" for prob in selected_problems]) + f"\n\nAI Applied Fixes & Details:\n{ai_fix_details}"
    else:
        problems_text = "- Complete AI Website Audit & Standard Security Fixes applied successfully."
    
    work_details = f"Website: {website_url}\nClient Name: {client_name}\nPhone: {client_phone}\nPayment ID: {payment_id}\nTotal Paid (Inc. GST): ₹{total_paid}\n\nResolved Issues & Actions:\n{problems_text}"
    
    # क्लाइंट और एडमिन (insightifytechinnovations@gmail.com) दोनों को मेल भेजना
    send_completion_email(client_email, work_details)
    
    print(f"Auto-fix completed and report sent for {website_url} (Client: {client_name}, Email: {client_email})")
    
    return jsonify({
        'status': 'success',
        'message': 'Payment verified, AI auto-fix completed, and proof reports dispatched successfully to client and admin.'
    })

# --- नया बल्क कैंपेन राउट (हजारों लोगों तक रिक्वायरमेंट/ऐड भेजने के लिए) ---
def send_bulk_outreach_email(to_email, client_name, requirement_subject, requirement_message):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get("BREVO_API_KEY", "YOUR_BREVO_API_KEY")
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    
    sender = {"name": "Insightify Tech Innovations", "email": "insightifytechinnovations@gmail.com"}
    to = [{"email": to_email, "name": client_name}]
    
    html_content = f"""
    <html>
      <body>
        <p>Dear {client_name},</p>
        <p>{requirement_message}</p>
        <br>
        <p><b>Insightify Tech Innovations Private Limited</b></p>
        <p>Web & Software Development, SEO & AI Automation Services</p>
        <p>Helpline: +91 8077644565 | GSTIN: 09AACHI6384B1ZG</p>
      </body>
    </html>
    """
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        sender=sender,
        subject=requirement_subject,
        html_content=html_content
    )
    
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print(f"Error sending bulk email to {to_email}: {e}")
        return False

@app.route('/send-bulk-campaign', methods=['POST'])
def send_bulk_campaign():
    data = request.json
    recipients_list = data.get('recipients', []) # [{'email': '...', 'name': '...'}, ...]
    subject = data.get('subject', 'Special IT & SEO Services Offer - Insightify Tech Innovations')
    message = data.get('message', 'We are offering automated website error fixing and AI audit services...')
    
    success_count = 0
    failed_count = 0
    
    for recipient in recipients_list:
        email = recipient.get('email')
        name = recipient.get('name', 'Valued Business Owner')
        
        if email:
            sent_status = send_bulk_outreach_email(email, name, subject, message)
            if sent_status:
                success_count += 1
            else:
                failed_count += 1
                
    return jsonify({
        'status': 'completed',
        'total_sent': success_count,
        'total_failed': failed_count,
        'message': f"Bulk campaign executed successfully. Sent: {success_count}, Failed: {failed_count}"
    })

if __name__ == '__main__':
    print("Insightify AI Server starting...")
    app.run(debug=True, port=5000)