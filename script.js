const API_URL = "127.0.0.1:5000/query";  // Replace with your Render chatbot URL

function sendMessage() {
    let inputField = document.getElementById("user-input");
    let userMessage = inputField.value.trim();
    
    if (userMessage === "") return;
    
    // Display user message
    displayMessage(userMessage, "user");

    // Send request to chatbot API
    fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage })
    })
    .then(response => response.json())
    .then(data => {
        if (data.results) {
            displayMessage(JSON.stringify(data.results), "bot");
        } else if (data.total) {
            displayMessage("Total: " + data.total, "bot");
        } else if (data.total_sales) {
            displayMessage("Total Sales: $" + data.total_sales, "bot");
        } else {
            displayMessage("I didn't understand that.", "bot");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        displayMessage("Error connecting to chatbot.", "bot");
    });

    // Clear input
    inputField.value = "";
}

function displayMessage(message, sender) {
    let chatBox = document.getElementById("chat-box");
    let messageDiv = document.createElement("div");
    messageDiv.classList.add(sender === "user" ? "user-message" : "bot-message");
    messageDiv.innerText = message;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}
