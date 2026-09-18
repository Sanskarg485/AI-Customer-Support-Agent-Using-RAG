const chat = document.getElementById("chat");
const form = document.getElementById("chat-form");
const questionInput = document.getElementById("question");
const sendButton = document.getElementById("send");
const clearButton = document.getElementById("clear");
const statusElement = document.getElementById("status");
const meta = document.getElementById("meta");

let history = [];


function addMessage(role, text, sources = []) {
    const message = document.createElement("div");
    message.className = `message ${role}`;

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text;

    if (sources.length > 0) {
        const source = document.createElement("div");
        source.className = "sources";
        source.textContent =
            `Knowledge base: ${sources.join(", ")}`;

        bubble.appendChild(source);
    }

    message.appendChild(bubble);
    chat.appendChild(message);

    chat.scrollTop = chat.scrollHeight;
}


function setStatus(text, type) {
    statusElement.textContent = text;
    statusElement.className = `status ${type}`;
}


async function checkHealth() {
    try {
        const response = await fetch("/api/health");

        if (!response.ok) {
            throw new Error("API unavailable");
        }

        setStatus("● Online", "online");
    } catch {
        setStatus("● Offline", "offline");
    }
}


async function sendQuestion(value) {
    const question = value.trim();

    if (!question || sendButton.disabled) {
        return;
    }

    addMessage("user", question);

    history.push({
        role: "user",
        content: question
    });

    questionInput.value = "";
    sendButton.disabled = true;
    meta.textContent = "Searching ChromaDB...";

    const thinkingMessage = document.createElement("div");
    thinkingMessage.className = "message assistant";

    const thinkingBubble = document.createElement("div");
    thinkingBubble.className = "bubble";
    thinkingBubble.textContent =
        "Searching the knowledge base...";

    thinkingMessage.appendChild(thinkingBubble);
    chat.appendChild(thinkingMessage);

    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question,
                history: history
            })
        });

        const data = await response.json();

        thinkingMessage.remove();

        if (!response.ok) {
            throw new Error(
                data.detail || "Request failed."
            );
        }

        addMessage(
            "assistant",
            data.answer,
            data.sources || []
        );

        history.push({
            role: "assistant",
            content: data.answer
        });

        meta.textContent =
            `${data.response_time_ms} ms`;

    } catch (error) {
        thinkingMessage.remove();

        addMessage(
            "assistant",
            `Sorry, I could not process your request.\n\n${error.message}`
        );

        meta.textContent = "Request failed";
    }

    sendButton.disabled = false;
    questionInput.focus();
}


form.addEventListener("submit", function (event) {
    event.preventDefault();
    sendQuestion(questionInput.value);
});


document
    .querySelectorAll(".suggestions button")
    .forEach((button) => {
        button.addEventListener("click", () => {
            sendQuestion(button.dataset.question);
        });
    });


clearButton.addEventListener("click", () => {
    history = [];

    chat.innerHTML = "";

    addMessage(
        "assistant",
        "Conversation cleared. How can I help you?"
    );

    meta.textContent = "Ready";
});


questionInput.addEventListener("keydown", (event) => {
    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {
        event.preventDefault();
        form.requestSubmit();
    }
});


checkHealth();
questionInput.focus();
