// Safe declaration to prevent duplicate identifier error
const chatContainer = document.getElementById('chatContainer');
const userInput = document.getElementById('user-input');

function toggleExpand(e) {
    if (e) e.stopPropagation();
    if (!chatContainer) return;
    chatContainer.classList.toggle('expanded');
    let btn = document.getElementById('expandBtn');
    if (btn) {
        btn.innerHTML = chatContainer.classList.contains('expanded') ? `<i class="bi bi-arrows-angle-contract"></i> छोटा करें` : `<i class="bi bi-arrows-angle-expand"></i> बड़ा करें`;
    }
}

if (userInput) {
    userInput.addEventListener('focus', function() {
        if (chatContainer) chatContainer.classList.add('expanded');
        let expandBtn = document.getElementById('expandBtn');
        if (expandBtn) expandBtn.innerHTML = `<i class="bi bi-arrows-angle-contract"></i> छोटा करें`;
    });

    // Enter बटन दबाने पर भी मैसेज सेंड होने के लिए फीचर जोड़ा गया है
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
}

function sendMessage() {
    let input = document.getElementById('user-input');
    let chatBox = document.getElementById('chat-box');
    if (!input || !chatBox) return;
    
    let messageText = input.value.trim();
    if (!messageText) return;

    chatBox.innerHTML += `<div class="mb-3 text-end"><div class="user-message-bubble d-inline-block text-start"><b>You:</b> ${messageText}</div></div>`;
    input.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: messageText })
    })
    .then(response => response.json())
    .then(data => {
        chatBox.innerHTML += `<div class="mb-3"><div class="ai-message-bubble d-inline-block"><strong class="text-info">Insightify AI Expert</strong><br>${data.response}</div></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        chatBox.innerHTML += `<div class="mb-3"><div class="ai-message-bubble d-inline-block"><strong class="text-info">Insightify AI Expert</strong><br>संपर्क करें: 8077644565</div></div>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    });
}

function calculateTotal() {
    let totalInr = 0;
    document.querySelectorAll('.problem-chk:checked').forEach(chk => {
        totalInr += parseInt(chk.getAttribute('data-price')) || 0;
    });
    let totalElement = document.getElementById('totalAmountText');
    if (totalElement) {
        totalElement.innerText = '₹' + totalInr.toLocaleString('en-IN');
    }
}

function handleScanSubmit(event) {
    event.preventDefault(); 
    let nameElem = document.getElementById('name');
    let emailElem = document.getElementById('email');
    let phoneElem = document.getElementById('phone');
    let webElem = document.getElementById('website');
    let reqElem = document.getElementById('requirements');

    let resName = document.getElementById('resName');
    let resUrl = document.getElementById('resUrl');

    if (resName) resName.innerText = nameElem ? nameElem.value || "Valued User" : "Valued User";
    if (resUrl) resUrl.innerText = webElem ? webElem.value || "https://..." : "https://...";
    
    let clientData = {
        name: nameElem ? nameElem.value : "",
        email: emailElem ? emailElem.value : "",
        phone: phoneElem ? phoneElem.value : "",
        website: webElem ? webElem.value : "",
        requirements: reqElem ? reqElem.value : ""
    };

    fetch('/send-report', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(clientData)
    })
    .then(response => response.json())
    .then(data => {
        console.log("Email report response:", data);
    })
    .catch(error => {
        console.error("Error sending email report:", error);
    });

    // पॉपअप दिखाने के साथ ही फ्रंट पेज के फॉर्म इनपुट्स को तुरंत साफ़ (clear) करने के लिए कोड
    let formEl = document.querySelector('form'); // या अपने लीड फॉर्म की आईडी यहाँ दें
    if (formEl) {
        formEl.reset();
    }

    let modalEl = document.getElementById('scanResultModal');
    if (modalEl && typeof bootstrap !== 'undefined') {
        new bootstrap.Modal(modalEl).show();
    }
}

function paySelectedProblems() {
    let totalInr = 0;
    let selectedList = [];
    document.querySelectorAll('.problem-chk:checked').forEach(chk => {
        totalInr += parseInt(chk.getAttribute('data-price')) || 0;
        selectedList.push(chk.getAttribute('data-name') || chk.value);
    });
    
    if(totalInr === 0) { alert("कृपया कम से कम एक समस्या (Problem) चुनें!"); return; }
    
    let nameElem = document.getElementById('name');
    let emailElem = document.getElementById('email');
    let phoneElem = document.getElementById('phone');
    let webElem = document.getElementById('website');

    var options = {
        "key": "rzp_live_TUiu15xHh1ZWpr",
        "amount": totalInr * 100, 
        "currency": "INR",
        "name": "Insightify Tech Innovations",
        "description": "Selected AI Website Audit Solutions (" + selectedList.length + " items)",
        "handler": function (response){
            alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
            
            // --- पेमेंट सफल होते ही बैकएंड पर डेटा सेव और ऑटो-फिक्स रिपोर्ट ट्रिगर करने का कोड ---
            fetch('/process-autofix', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    payment_id: response.razorpay_payment_id,
                    name: nameElem ? nameElem.value : "Valued Client",
                    email: emailElem ? emailElem.value : "insightifytechinnovations@gmail.com",
                    phone: phoneElem ? phoneElem.value : "8077644565",
                    website: webElem ? webElem.value : "https://insightifyinnovations.com",
                    selected_problems: selectedList,
                    total: totalInr
                })
            })
            .then(res => res.json())
            .then(resData => {
                console.log("Auto-fix and email report dispatched:", resData);
            })
            .catch(err => console.error("Auto-fix error:", err));
        },
        "prefill": {
            "name": nameElem ? nameElem.value : "Valued Client",
            "email": emailElem ? emailElem.value : "insightifytechinnovations@gmail.com",
            "contact": phoneElem ? phoneElem.value : "8077644565"
        },
        "theme": { "color": "#38bdf8" }
    };
    new Razorpay(options).open();
}

function payWithRazorpay() {
    let payAmountElem = document.getElementById('payAmount');
    let amountVal = payAmountElem ? payAmountElem.value || 999 : 999;
    
    let nameElem = document.getElementById('name');
    let emailElem = document.getElementById('email');
    let phoneElem = document.getElementById('phone');
    let webElem = document.getElementById('website');

    var options = {
        "key": "rzp_live_TUiu15xHh1ZWpr",
        "amount": amountVal * 100, 
        "currency": "INR",
        "name": "Insightify Tech Innovations",
        "description": "SEO & AI Services Consultation Fee",
        "handler": function (response){
            alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
            
            fetch('/process-autofix', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    payment_id: response.razorpay_payment_id,
                    name: nameElem ? nameElem.value : "Valued Client",
                    email: emailElem ? emailElem.value : "insightifytechinnovations@gmail.com",
                    phone: phoneElem ? phoneElem.value : "8077644565",
                    website: webElem ? webElem.value : "https://insightifyinnovations.com",
                    selected_problems: ["Standard SEO Consultation & General Fixes"],
                    total: amountVal
                })
            })
            .then(res => res.json())
            .then(resData => console.log("Consultation report sent:", resData))
            .catch(err => console.error("Error:", err));
        },
        "prefill": {
            "name": nameElem ? nameElem.value : "Valued Client",
            "email": emailElem ? emailElem.value : "insightifytechinnovations@gmail.com",
            "contact": phoneElem ? phoneElem.value : "8077644565"
        },
        "theme": { "color": "#38bdf8" }
    };
    new Razorpay(options).open();
}

let currentIndex = 1;
const totalImages = 5; 

function changeBannerImage() {
    currentIndex = currentIndex > totalImages ? 1 : currentIndex;
    const bannerImg = document.getElementById('dynamic-banner');
    if (bannerImg) {
        bannerImg.src = `/static/images/img${currentIndex}.png`;
    }
    currentIndex++;
}

setInterval(changeBannerImage, 3000);