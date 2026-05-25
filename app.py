from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import smtplib
from email.message import EmailMessage
from ai_engine import generate_code_for_client  # सुनिश्चित करें ai_engine.py साथ में है

app = Flask(__name__)

# डेटाबेस सेटअप
def init_db():
    conn = sqlite3.connect('insightify_data.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS orders 
                      (id INTEGER PRIMARY KEY, name TEXT, phone TEXT, 
                       firm_name TEXT, gstin TEXT, requirements TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/<page_name>')
def show_page(page_name):
    try:
        return render_template(f'{page_name}.html')
    except:
        return "यह पेज अभी बन रहा है!", 404

@app.route('/submit-order', methods=['POST'])
def submit_order():
    data = request.json
    
    # 1. डेटाबेस में सेव करें
    conn = sqlite3.connect('insightify_data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (name, phone, firm_name, gstin, requirements) VALUES (?,?,?,?,?)",
                   (data['name'], data['phone'], data['firm_name'], data['gstin'], data['requirements']))
    conn.commit()
    conn.close()
    
    # 2. AI से जवाब लें
    ai_response = generate_code_for_client(data['requirements'])
    
    # 3. ईमेल भेजें
    msg = EmailMessage()
    msg['Subject'] = f"New Client Order: {data['firm_name']}"
    msg['From'] = 'insightifytechinnovations@gmail.com'
    msg['To'] = 'insightifytechinnovations@gmail.com'
    body = f"नया ऑर्डर प्राप्त हुआ:\n\nनाम: {data['name']}\nविवरण: {data['requirements']}\n\nAI का सुझाव: {ai_response}"
    msg.set_content(body)
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login('insightifytechinnovations@gmail.com', 'vkoiupmjppfukern')
        smtp.send_message(msg)
        
    return jsonify({"status": "success", "ai_answer": ai_response})

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

# यहाँ app.run() की जरूरत नहीं है, Render अपना सर्वर खुद चलाएगा