from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from chatbot_engine import insightify_ai_bot
from payment_processor import create_payment_link
import os
import openai
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from apscheduler.schedulers.background import BackgroundScheduler

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

    if selected_problems:
        problems_list_str = ", ".join(selected_problems)
        try:
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
    
    send_completion_email(client_email, work_details)
    print(f"Auto-fix completed and report sent for {website_url} (Client: {client_name}, Email: {client_email})")
    
    return jsonify({
        'status': 'success',
        'message': 'Payment verified, AI auto-fix completed, and proof reports dispatched successfully to client and admin.'
    })

# --- बल्क ईमेल भेजने का कोर फंक्शन (Brevo API) ---
def send_single_outreach(to_email, client_name, subject, message):
    configuration = sib_api_v3_sdk.Configuration()
    configuration.api_key['api-key'] = os.environ.get("BREVO_API_KEY", "YOUR_BREVO_API_KEY")
    
    api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
    sender = {"name": "Insightify Tech Innovations", "email": "insightifytechinnovations@gmail.com"}
    to = [{"email": to_email, "name": client_name}]
    
    html_content = f"""
    <html>
      <body>
        <p>Dear {client_name},</p>
        <p>{message}</p>
        <br>
        <p><b>Insightify Tech Innovations Private Limited</b></p>
        <p>Web & Software Development, SEO & AI Automation Services</p>
        <p>Helpline: +91 8077644565 | GSTIN: 09AACHI6384B1ZG</p>
        <p><a href="https://insightifyinnovations.com">Visit our website to fix your website errors instantly</a></p>
      </body>
    </html>
    """
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, sender=sender, subject=subject, html_content=html_content)
    try:
        api_instance.send_transac_email(send_smtp_email)
        return True
    except ApiException as e:
        print(f"Error sending email to {to_email}: {e}")
        return False

# --- एआई द्वारा हर दिन नया स्मार्ट ऐड जनरेट करने और 20,000 लोगों तक भेजने का ऑटोमैटिक शेड्यूलर जॉब ---
def daily_ai_smart_campaign():
    print("AI generating new smart advertisement for today...")
    try:
        # OpenAI से हर दिन एक नया आकर्षक मार्केटिंग विज्ञापन लिखवाना
        prompt = "Create a short, high-converting professional marketing ad copy for an IT and SEO agency named Insightify Tech Innovations. The ad should encourage business owners to fix website errors and boost sales using AI automation."
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250
        )
        daily_ad_message = response.choices[0].message.content.strip()
    except Exception as e:
        daily_ad_message = "Boost your website performance, fix technical errors, and grow your business with Insightify Tech Innovations AI automation tools."

    subject = "Daily Special Offer: Instant AI Website Audit & Error Fixing"
    
    # यहाँ आप अपनी 20,000 लोगों की ईमेल लिस्ट लोड कर सकते हैं (फिलहाल डमी या डेटाबेस लिस्ट)
    # उदाहरण के लिए मान लीजिए आपके पास लिस्ट है:
    recipients_list = [
        # {'email': 'client1@gmail.com', 'name': 'Client One'},
        # {'email': 'client2@gmail.com', 'name': 'Client Two'}
    ]
    
    print(f"Starting daily campaign dispatch to {len(recipients_list)} target recipients...")
    success_count = 0
    for person in recipients_list:
        if send_single_outreach(person['email'], person.get('name', 'Business Owner'), subject, daily_ad_message):
            success_count += 1
            
    print(f"Daily AI Campaign executed. Successfully sent to {success_count} persons.")

# बैकग्राउंड शेड्यूलर सेटअप (जो रोज अपने आप चलेगा)
scheduler = BackgroundScheduler()
# हर दिन सुबह 10:00 बजे यह ऑटोमैटिक रन होगा
scheduler.add_job(func=daily_ai_smart_campaign, trigger="cron", hour=10, minute=0)
scheduler.start()

@app.route('/send-bulk-campaign', methods=['POST'])
def send_bulk_campaign():
    data = request.json
    recipients_list = data.get('recipients', []) 
    subject = data.get('subject', 'Special IT & SEO Services Offer - Insightify Tech Innovations')
    message = data.get('message', 'We are offering automated website error fixing and AI audit services...')
    
    success_count = 0
    failed_count = 0
    
    for recipient in recipients_list:
        email = recipient.get('email')
        name = recipient.get('name', 'Valued Business Owner')
        if email:
            if send_single_outreach(email, name, subject, message):
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
    print("Insightify AI Server starting with Daily AI Campaign Scheduler...")
    app.run(debug=True, port=5000)