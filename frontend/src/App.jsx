import { useState, useRef, useEffect } from "react";

const API_URL = "https://tgmck07lq0.execute-api.us-east-1.amazonaws.com/prod/chat";
const SESSION_ID = `session-${Date.now()}`;

function Message({ role, text }) {
  return (
    <div style={{
      display: "flex",
      justifyContent: role === "user" ? "flex-end" : "flex-start",
      marginBottom: "12px"
    }}>
      <div style={{
        maxWidth: "70%",
        padding: "12px 16px",
        borderRadius: role === "user" ? "18px 18px 4px 18px" : "18px 18px 18px 4px",
        backgroundColor: role === "user" ? "#1a1a2e" : "#f0f0f0",
        color: role === "user" ? "#ffffff" : "#1a1a2e",
        fontSize: "14px",
        lineHeight: "1.5",
        whiteSpace: "pre-wrap"
      }}>
        {text}
      </div>
    </div>
  );
}

export default function App() {
  const [messages, setMessages] = useState([
    { role: "agent", text: "Hi! I can look up order status and shipment updates. Ask me about an order ID or a customer name." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage() {
    const query = input.trim();
    if (!query || loading) return;

    setMessages(prev => [...prev, { role: "user", text: query }]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query, session_id: SESSION_ID })
      });

      const data = await res.json();
      const reply = data.response || data.error || "No response received.";
      setMessages(prev => [...prev, { role: "agent", text: reply }]);
    } catch (err) {
      setMessages(prev => [...prev, { role: "agent", text: "Error reaching the agent. Please try again." }]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      maxWidth: "720px",
      margin: "0 auto",
      fontFamily: "'Inter', sans-serif",
      backgroundColor: "#ffffff"
    }}>
      {/* Header */}
      <div style={{
        padding: "16px 24px",
        borderBottom: "1px solid #e5e5e5",
        backgroundColor: "#1a1a2e",
        color: "#ffffff"
      }}>
        <div style={{ fontSize: "16px", fontWeight: "600" }}>Customer Service Agent</div>
        <div style={{ fontSize: "12px", color: "#aaaacc", marginTop: "2px" }}>Order & Shipment Lookup</div>
      </div>

      {/* Messages */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "24px 16px"
      }}>
        {messages.map((m, i) => (
          <Message key={i} role={m.role} text={m.text} />
        ))}
        {loading && (
          <div style={{ display: "flex", justifyContent: "flex-start", marginBottom: "12px" }}>
            <div style={{
              padding: "12px 16px",
              borderRadius: "18px 18px 18px 4px",
              backgroundColor: "#f0f0f0",
              color: "#888",
              fontSize: "14px"
            }}>
              Looking up...
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div style={{
        padding: "16px",
        borderTop: "1px solid #e5e5e5",
        display: "flex",
        gap: "8px"
      }}>
        <textarea
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask about an order or customer..."
          rows={1}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #e5e5e5",
            fontSize: "14px",
            resize: "none",
            outline: "none",
            fontFamily: "inherit"
          }}
        />
        <button
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            backgroundColor: loading || !input.trim() ? "#cccccc" : "#1a1a2e",
            color: "#ffffff",
            fontSize: "14px",
            cursor: loading || !input.trim() ? "not-allowed" : "pointer",
            fontFamily: "inherit"
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}