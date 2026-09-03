import os
import razorpay

# Apni Razorpay Key aur Secret yahan daalein (या Render एनवायरनमेंट से उठाएं)
RAZORPAY_KEY_ID = os.environ.get("RAZORPAY_KEY_ID", "rzp_live_TUiu15xHh1ZWpr")
RAZORPAY_KEY_SECRET = os.environ.get("RAZORPAY_KEY_SECRET", "0CZVyPk7zp1odbOruc9WzzB7")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_payment_link(amount, client_name, client_email, client_phone):
    """
    18% GST add karke final amount calculate karna aur Razorpay payment link generate karna.
    """
    try:
        gst_rate = 0.18
        # Base amount par 18% GST जोड़कर Razorpay के लिए पैसे (Paise) में कन्वर्ट करना (₹1 = 100 paise)
        total_amount = int(float(amount) * (1 + gst_rate) * 100)
        
        payment_data = {
            "amount": total_amount,
            "currency": "INR",
            "accept_partial": False,
            "description": "Insightify Tech Innovations - AI Service Payment & GST Invoice",
            "customer": {
                "name": client_name or "Valued Client",
                "email": client_email or "insightifytechinnovations@gmail.com",
                "contact": client_phone or "9876543210"
            },
            "notify": {"sms": True, "email": True},
            "reminder_enable": True,
            "callback_url": "https://insightifyinnovations.com/payment-success",
            "callback_method": "get"
        }
        
        response = client.payment_link.create(payment_data)
        return response
        
    except Exception as e:
        print(f"Razorpay Payment Link Error: {e}")
        # अगर एपीआई में कोई दिक्कत आए, तो फॉलबैक के लिए डमी लिंक रिटर्न करना ताकि ऐप क्रैश न हो
        return {
            "short_url": f"https://rzp.io/i/insightify?error=failed"
        }