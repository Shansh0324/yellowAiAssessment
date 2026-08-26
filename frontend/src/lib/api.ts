const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export async function sendMessage(sessionId: string, customerId: string, message: string) {
  const response = await fetch(`${API_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      session_id: sessionId,
      customer_id: customerId,
      message,
    }),
  });

  if (!response.ok) {
    throw new Error('Failed to send message');
  }

  return response.json();
}

export async function getCustomerSessions(customerId: string) {
  const response = await fetch(`${API_URL}/sessions/customer/${customerId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch sessions');
  }
  return response.json();
}

export async function getSession(sessionId: string) {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`);
  if (!response.ok) {
    throw new Error('Failed to fetch session');
  }
  return response.json();
}

export async function deleteSession(sessionId: string) {
  const response = await fetch(`${API_URL}/sessions/${sessionId}`, {
    method: 'DELETE',
  });
  if (!response.ok) {
    throw new Error('Failed to delete session');
  }
  return response.json();
}
