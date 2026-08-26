<script>
    // --- नए फीचर्स: देश पहचान और अलग-अलग प्राइस कैलकुलेशन के लिए ग्लोबल वेरिएबल्स ---
    let currentCurrencySymbol = '₹';
    let currencyMultiplier = 1;

    // 1. देश पहचान कर करेंसी सेट करने का फंक्शन
    async function detectCountryAndSetCurrency() {
        try {
            let response = await fetch('https://ipapi.co/json/');
            let data = await response.json();
            let country = data.country_code; // जैसे 'US', 'IN'
            
            if (country === 'US') {
                currentCurrencySymbol = '$';
                currencyMultiplier = 1 / 83; // 1 USD = 83 INR अनुमानित दर
            } else {
                currentCurrencySymbol = '₹';
                currencyMultiplier = 1;
            }
            updateAllPricesDisplay();
        } catch (e) {
            console.log('Geo-IP detection default to INR');
        }
    }

    // सभी प्राइसेस को रिफ्रेश और अपडेट करने का फंक्शन
    function updateAllPricesDisplay() {
        document.querySelectorAll('.dynamic-price').forEach(el => {
            let baseInr = parseFloat(el.getAttribute('data-inr')) || 0;
            let finalVal = baseInr * currencyMultiplier;
            if (currentCurrencySymbol === '$') {
                el.innerText = '$' + finalVal.toFixed(2);
            } else {
                el.innerText = '₹' + baseInr.toLocaleString('en-IN');
            }
        });
        calculateTotal();
    }

    // चुनी गई समस्याओं का अलग-अलग प्राइस जोड़कर कुल योग निकालने का फंक्शन
    function calculateTotal() {
        let totalInr = 0;
        document.querySelectorAll('.problem-chk:checked').forEach(chk => {
            totalInr += parseInt(chk.getAttribute('data-price')) || 0;
        });
        
        let totalElement = document.getElementById('totalAmountText');
        if (totalElement) {
            totalElement.setAttribute('data-inr', totalInr);
            let displayVal = totalInr * currencyMultiplier;
            if (currentCurrencySymbol === '$') {
                totalElement.innerText = '$' + displayVal.toFixed(2);
            } else {
                totalElement.innerText = '₹' + totalInr.toLocaleString('en-IN');
            }
        }
    }

    // चुनी गई समस्याओं के साथ Razorpay पेमेंट ट्रिगर करने का फंक्शन (अलग-अलग प्राइस के आधार पर)
    function paySelectedProblems() {
        let totalInr = 0;
        let selectedList = [];
        document.querySelectorAll('.problem-chk:checked').forEach(chk => {
            totalInr += parseInt(chk.getAttribute('data-price')) || 0;
            selectedList.push(chk.getAttribute('data-name'));
        });
        
        if(totalInr === 0) { 
            alert("कृपया कम से कम एक समस्या (Problem) चुनें!"); 
            return; 
        }
        
        let payableAmountInr = totalInr;

        let options = {
            "key": "rzp_live_S14t63o9aY77yZ", 
            "amount": payableAmountInr * 100, // हमेशा पैसे (Paise) में INR बेस वैल्यू जाती है
            "currency": "INR",
            "name": "Insightify Tech Innovations",
            "description": "Selected AI Website Audit & Auto-Fix Solutions (" + selectedList.length + " items)",
            "image": "/static/images/img1.png",
            "handler": function (response){
                alert("भुगतान सफल रहा! Payment ID: " + response.razorpay_payment_id);
            },
            "prefill": {
                "name": "Vikash Agrawal",
                "email": "insightifytechinnovations@gmail.com",
                "contact": "8077644565"
            },
            "theme": {
                "color": "#38bdf8"
            }
        };
        
        if (typeof Razorpay !== 'undefined') {
            let rzp1 = new Razorpay(options);
            rzp1.open();
        } else {
            alert("Razorpay SDK loaded incorrectly or missing.");
        }
    }

    // --- आपकी पुरानी सभी कोडिंग (बिना किसी बदलाव के सुरक्षित) ---

    // Existing sendMessage function support for chat input enter key or button click
    function sendMessage() {
        let userInput = document.getElementById('user-input');
        let chatBox = document.getElementById('chat-box');
        
        if (!userInput || !userInput.value.trim()) return;
        
        let messageText = userInput.value.trim();
        
        // Append user message to chat box
        chatBox.innerHTML += `<div class="mb-3 text-end">
            <div class="user-message-bubble d-inline-block bg-info text-dark p-2 rounded" style="max-width: 92%;">
                ${messageText}
            </div>
        </div>`;
        
        userInput.value = '';
        chatBox.scrollTop = chatBox.scrollHeight;
        
        // Send POST request to backend Flask /chat endpoint
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            chatBox.innerHTML += `<div class="mb-3">
                <div class="ai-message-bubble d-inline-block p-2 rounded bg-dark text-light border border-info" style="max-width: 92%;">
                    <div class="d-flex align-items-center mb-1">
                        <i class="bi bi-cpu-fill text-info me-2"></i>
                        <strong class="text-info">Insightify AI Expert</strong>
                    </div>
                    ${data.reply}
                </div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        })
        .catch(error => {
            console.error('Chat Error:', error);
            chatBox.innerHTML += `<div class="mb-3">
                <div class="ai-message-bubble d-inline-block border-danger p-2 rounded bg-dark text-light" style="max-width: 92%;">
                    <div class="d-flex align-items-center mb-1">
                        <i class="bi bi-exclamation-triangle-fill text-danger me-2"></i>
                        <strong class="text-danger">System Error</strong>
                    </div>
                    क्षमा करें, सर्वर से संपर्क करने में समस्या आ रही है। कृपया सीधे कॉल करें: <strong>+91 8077644565</strong>
                </div>
            </div>`;
            chatBox.scrollTop = chatBox.scrollHeight;
        });
    }

    function handleScanSubmit(event) {
        event.preventDefault();
        
        let form = document.getElementById('seo-form');
        let formData = new FormData(form);
        
        let name = formData.get('Name');
        let url = formData.get('Website_URL');
        
        let resNameEl = document.getElementById('resName');
        let resUrlEl = document.getElementById('resUrl');
        
        if (resNameEl) resNameEl.innerText = name || 'Valued Client';
        if (resUrlEl) resUrlEl.innerText = url || 'https://...';
        
        // Submit via fetch to FormSubmit endpoint without navigating away
        fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        }).then(response => {
            let scanModalElement = document.getElementById('seo-form') && document.getElementById('scanResultModal');
            if (scanModalElement && typeof bootstrap !== 'undefined') {
                let scanModal = new bootstrap.Modal(scanModalElement);
                scanModal.show();
            }
            form.reset();
        }).catch(error => {
            console.error('Submission Error:', error);
            let scanModalElement = document.getElementById('scanResultModal');
            if (scanModalElement && typeof bootstrap !== 'undefined') {
                let scanModal = new bootstrap.Modal(scanModalElement);
                scanModal.show();
            }
            form.reset();
        });
    }

    function payWithRazorpay() {
        let totalInr = 0;
        let selectedList = [];
        document.querySelectorAll('.problem-chk:checked').forEach(chk => {
            totalInr += parseInt(chk.getAttribute('data-price')) || 0;
            selectedList.push(chk.getAttribute('data-name'));
        });
        
        // यदि यूजर ने कोई समस्या नहीं चुनी है, तो डिफ़ॉल्ट 999 ले, अन्यथा कुल योग लें
        let amountVal = totalInr > 0 ? totalInr : 999;
        
        let nameInput = document.getElementById('name');
        let emailInput = document.getElementById('email');
        let phoneInput = document.getElementById('phone');

        let options = {
            "key": "rzp_live_TLGQmCY5RuAV2e", 
            "amount": amountVal * 100, // Amount in paise
            "currency": "INR",
            "name": "Insightify Tech Innovations",
            "description": selectedList.length > 0 ? "Selected AI Solutions (" + selectedList.length + " items)" : "Global AI SEO & IT Services Consultation",
            "image": "/static/images/img1.png",
            "handler": function (response){
                alert("भुगतान सफल रहा! Payment ID: " + response.razorpay_payment_id);
            },
            "prefill": {
                "name": nameInput ? (nameInput.value || "Vikash Agrawal") : "Vikash Agrawal",
                "email": emailInput ? (emailInput.value || "insightifytechinnovations@gmail.com") : "insightifytechinnovations@gmail.com",
                "contact": phoneInput ? (phoneInput.value || "8077644565") : "8077644565"
            },
            "theme": {
                "color": "#38bdf8"
            }
        };
        
        if (typeof Razorpay !== 'undefined') {
            let rzp1 = new Razorpay(options);
            rzp1.open();
        } else {
            alert("Razorpay SDK loaded incorrectly or missing.");
        }
    }

    // पेज लोड होते ही देश पहचान कर करेंसी सेट करने का ऑटो-ट्रिगर
    window.addEventListener('DOMContentLoaded', () => {
        detectCountryAndSetCurrency();
    });
</script>
</body>
</html>