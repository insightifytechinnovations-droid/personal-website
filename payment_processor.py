import razorpay

# Apni Razorpay Key aur Secret yahan daalein
client = razorpay.Client(auth=("rzp_test_T6DoFTJE5c9RgO", "345x3JjgH90YRPXWM4mzyGVF"))

def create_payment_link(amount, client_name, client_email, client_phone):
    """
    18% GST add karke final amount calculate karna aur payment link generate karna.
    """
    gst_rate = 0.18
    total_amount = int(amount * (1 + gst_rate)) * 100  # Paise mein convert karna
    
    payment_data = {
        "amount": total_amount,
        "currency": "INR",
        "accept_partial": False,
        "description": "Insightify Tech Innovations - AI Service Payment",
        "customer": {
            "name": client_name,
            "email": client_email,
            "contact": client_phone
        },
        "notify": {"sms": True, "email": True},
        "reminder_enable": True,
        "callback_url": "https://yourdomain.com/payment-success/",
        "callback_method": "get"
    }
    
    return client.payment_link.create(payment_data)