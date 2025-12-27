import React, { useState, useEffect, useRef } from "react";
import { createSession, sendMessage } from "../sessionservice";
import "./Chat.css";

export default function Chat() {
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [initializing, setInitializing] = useState(true);
  const messagesEndRef = useRef(null);
  const chatContainerRef = useRef(null);

  useEffect(() => {
    (async () => {
      try {
        setInitializing(true);
        const sid = await createSession();
        setSessionId(sid);
        setError(null);
      } catch (err) {
        setError("Failed to initialize session. Please check if the backend server is running.");
        console.error("Session creation error:", err);
      } finally {
        setInitializing(false);
      }
    })();
  }, []);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  async function handleSend(e) {
    e.preventDefault();
    if (!text.trim() || !sessionId || loading) return;
    
    const userMsg = { role: "user", text: text.trim() };
    setMessages(prev => [...prev, userMsg]);
    setText("");
    setLoading(true);
    setError(null);

    try {
      const r = await sendMessage(sessionId, userMsg.text);
      const reply = r.reply;
      setMessages(prev => [...prev, { role: "agent", text: reply }]);
    } catch (err) {
      setError("Failed to send message. Please try again.");
      console.error("Message send error:", err);
      // Remove the user message if sending failed
      setMessages(prev => prev.filter((msg, idx) => !(idx === prev.length - 1 && msg.role === "user")));
    } finally {
      setLoading(false);
    }
  }

  if (initializing) {
    return (
      <div className="chat-container">
        <div className="loading-screen">
          <div className="spinner"></div>
          <p>Initializing chat session...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-card">
        {/* Header */}
        <div className="chat-header">
          <div className="header-content">
            <div className="header-icon">🏥</div>
            <div>
              <h1>Medical Consultation</h1>
              <p className="header-subtitle">AI Patient Simulation</p>
            </div>
          </div>
        </div>

        {/* Error Message */}
        {error && (
          <div className="error-message fade-in">
            <span className="error-icon">⚠️</span>
            {error}
          </div>
        )}

        {/* Messages Area */}
        <div className="messages-container" ref={chatContainerRef}>
          {messages.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon">💬</div>
              <h3>Start the Conversation</h3>
              <p>Begin by asking the patient about their symptoms or concerns.</p>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((m, i) => (
                <div 
                  key={i} 
                  className={`message fade-in ${m.role === "user" ? "message-user" : "message-patient"}`}
                >
                  <div className="message-avatar">
                    {m.role === "user" ? "👨‍⚕️" : "👤"}
                  </div>
                  <div className="message-content">
                    <div className="message-header">
                      <span className="message-sender">
                        {m.role === "user" ? "Doctor" : "Patient"}
                      </span>
                    </div>
                    <div className="message-text">{m.text}</div>
                  </div>
                </div>
              ))}
              {loading && (
                <div className="message message-patient typing-indicator">
                  <div className="message-avatar">👤</div>
                  <div className="message-content">
                    <div className="typing-dots">
                      <span></span>
                      <span></span>
                      <span></span>
                    </div>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <form onSubmit={handleSend} className="input-area">
          <div className="input-wrapper">
            <input
              type="text"
              value={text}
              onChange={e => setText(e.target.value)}
              placeholder="Type your message here..."
              disabled={loading || !sessionId}
              className="message-input"
            />
            <button
              type="submit"
              disabled={loading || !sessionId || !text.trim()}
              className="send-button"
            >
              {loading ? (
                <span className="button-loading">⏳</span>
              ) : (
                <span className="button-icon">📤</span>
              )}
              <span className="button-text">{loading ? "Sending..." : "Send"}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
