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

    // Enter बटन दबाने पर भी मैसेज सेंड होने के लिए फीचर जोड़ा गया है
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
    let webElem = document.getElementById('website');
    let resName = document.getElementById('resName');
    let resUrl = document.getElementById('resUrl');

    if (resName) resName.innerText = nameElem ? nameElem.value || "Valued User" : "Valued User";
    if (resUrl) resUrl.innerText = webElem ? webElem.value || "https://..." : "https://...";
    
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
        selectedList.push(chk.getAttribute('data-name'));
    });
    
    if(totalInr === 0) { alert("कृपया कम से कम एक समस्या (Problem) चुनें!"); return; }
    
    let nameElem = document.getElementById('name');
    let emailElem = document.getElementById('email');
    let phoneElem = document.getElementById('phone');

    var options = {
        "key": "rzp_live_TUiu15xHh1ZWpr",
        "amount": totalInr * 100, 
        "currency": "INR",
        "name": "Insightify Tech Innovations",
        "description": "Selected AI Website Audit Solutions (" + selectedList.length + " items)",
        "handler": function (response){
            alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
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

    var options = {
        "key": "rzp_live_TUiu15xHh1ZWpr",
        "amount": amountVal * 100, 
        "currency": "INR",
        "name": "Insightify Tech Innovations",
        "description": "SEO & AI Services Consultation Fee",
        "handler": function (response){
            alert("Payment Successful! Payment ID: " + response.razorpay_payment_id);
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