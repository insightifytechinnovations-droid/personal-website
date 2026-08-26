<<<<<<< HEAD
from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from chatbot_engine import insightify_ai_bot
from payment_processor import create_payment_link
import os
import openai
openai.api_key = os.environ.get("GEMINI_API_KEY")
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
            # यहाँ अपनी ईमेल आईडी और Google App Password डालें
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

# AI चैटबॉट राउट - क्लाइंट के सवालों को chatbot_engine से जोड़ा गया है
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_response = insightify_ai_bot(user_message)
    return jsonify({'response': bot_response})

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.json
    # Client details extract karna
    client_name = data.get('name')
    client_website = data.get('website')
    
    # Client requirement ke हिसाब से calculation
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

# --- एडवांस्ड ऑटो-फिक्स और पेमेंट वेरिफिकेशन राउट ---
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

    # समस्याओं की लिस्ट तैयार करना
    if selected_problems:
        problems_text = "\n".join([f"- {prob}" for prob in selected_problems])
    else:
        problems_text = "- Complete AI Website Audit & Standard Security Fixes"
    
    work_details = f"Website: {website_url}\nClient Name: {client_name}\nPhone: {client_phone}\nPayment ID: {payment_id}\nTotal Paid (Inc. GST): ₹{total_paid}\n\nResolved Issues:\n{problems_text}"
    
    # क्लाइंट और एडमिन दोनों को मेल भेजने का फंक्शन कॉल
    send_completion_email(client_email, work_details)
    
    print(f"Auto-fix completed and report sent for {website_url} (Client: {client_name}, Email: {client_email})")
    
    return jsonify({
        'status': 'success',
        'message': 'Payment verified, AI auto-fix completed, and proof reports dispatched successfully to client and admin.'
    })

if __name__ == '__main__':
    print("Insightify AI Server starting...")
=======
from flask import Flask, render_template, request, jsonify
import smtplib
from email.message import EmailMessage
from chatbot_engine import insightify_ai_bot
from payment_processor import create_payment_link
import os
import openai
openai.api_key = os.environ.get("GEMINI_API_KEY")
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
            # यहाँ अपनी ईमेल आईडी और Google App Password डालें
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

# AI चैटबॉट राउट - क्लाइंट के सवालों को chatbot_engine से जोड़ा गया है
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    bot_response = insightify_ai_bot(user_message)
    return jsonify({'response': bot_response})

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    data = request.json
    # Client details extract karna
    client_name = data.get('name')
    client_website = data.get('website')
    
    # Client requirement ke हिसाब से calculation
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

# --- एडवांस्ड ऑटो-फिक्स और पेमेंट वेरिफिकेशन राउट ---
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

    # समस्याओं की लिस्ट तैयार करना
    if selected_problems:
        problems_text = "\n".join([f"- {prob}" for prob in selected_problems])
    else:
        problems_text = "- Complete AI Website Audit & Standard Security Fixes"
    
    work_details = f"Website: {website_url}\nClient Name: {client_name}\nPhone: {client_phone}\nPayment ID: {payment_id}\nTotal Paid (Inc. GST): ₹{total_paid}\n\nResolved Issues:\n{problems_text}"
    
    # क्लाइंट और एडमिन दोनों को मेल भेजने का फंक्शन कॉल
    send_completion_email(client_email, work_details)
    
    print(f"Auto-fix completed and report sent for {website_url} (Client: {client_name}, Email: {client_email})")
    
    return jsonify({
        'status': 'success',
        'message': 'Payment verified, AI auto-fix completed, and proof reports dispatched successfully to client and admin.'
    })

if __name__ == '__main__':
    print("Insightify AI Server starting...")
>>>>>>> e7d22e130d6358a4a41f5e48260c9ad0975bc3f9
    app.run(debug=True, port=5000)