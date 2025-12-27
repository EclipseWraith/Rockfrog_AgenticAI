// Use VITE_API_URL if set (for production), otherwise empty string (uses Vite proxy for local dev)
const API_BASE_URL = import.meta.env.VITE_API_URL || "";

export async function createSession() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/session`, { 
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });
    if (!res.ok) {
      throw new Error(`Failed to create session: ${res.statusText}`);
    }
    const data = await res.json();
    return data.session_id;
  } catch (error) {
    console.error("Error creating session:", error);
    throw error;
  }
}

export async function sendMessage(session_id, text) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/message`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id, message: text })
    });
    if (!res.ok) {
      throw new Error(`Failed to send message: ${res.statusText}`);
    }
    return await res.json();
  } catch (error) {
    console.error("Error sending message:", error);
    throw error;
  }
}
