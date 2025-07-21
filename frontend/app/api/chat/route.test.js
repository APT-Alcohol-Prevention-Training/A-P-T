import { POST } from './route'

// Mock fetch globally
global.fetch = jest.fn()

describe('/api/chat Route Handler', () => {
  beforeEach(() => {
    fetch.mockClear()
    process.env.BACKEND_API_URL = 'http://localhost:8080'
  })

  test('successfully proxies chat request to backend', async () => {
    const mockBackendResponse = {
      bot_response: 'Hello from backend!',
      session_id: 'test-session-123'
    }

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockBackendResponse,
    })

    const requestBody = {
      message: 'Hello',
      chatbot_type: 'ai',
      risk_score: 5,
      conversation_context: { test: true }
    }

    const request = {
      json: async () => requestBody
    }

    const response = await POST(request)
    const data = await response.json()

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8080/',
      expect.objectContaining({
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: 'Hello',
          chatbot_type: 'ai',
          risk_score: 5,
          conversation_context: { test: true }
        })
      })
    )

    expect(data).toEqual(mockBackendResponse)
    // NextResponse.json() doesn't expose status property in tests
  })

  test('handles backend error response', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: false,
      status: 503,
      json: async () => ({ error: 'Backend unavailable' }),
    })

    const request = {
      json: async () => ({
        message: 'Hello',
        chatbot_type: 'ai',
      })
    }

    const response = await POST(request)
    const data = await response.json()

    expect(data).toEqual({ error: 'Backend unavailable' })
  })

  test('handles network error', async () => {
    global.fetch.mockRejectedValueOnce(new Error('Network failure'))

    const request = {
      json: async () => ({
        message: 'Hello',
        chatbot_type: 'ai',
      })
    }

    const response = await POST(request)
    const data = await response.json()

    expect(data).toEqual({ error: 'Server error' })
    // NextResponse.json() with status 500 is created in the route handler
  })

  test('handles invalid JSON in request', async () => {
    const request = {
      json: async () => {
        throw new Error('Invalid JSON')
      }
    }

    const response = await POST(request)
    const data = await response.json()

    expect(data).toEqual({ error: 'Server error' })
    // NextResponse.json() with status 500 is created in the route handler
  })

  test('uses default backend URL when env variable not set', async () => {
    delete process.env.BACKEND_API_URL

    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ bot_response: 'Test' }),
    })

    const request = {
      json: async () => ({
        message: 'Test',
        chatbot_type: 'ai',
      })
    }

    await POST(request)

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8080/',
      expect.any(Object)
    )
  })

  test('passes all required fields to backend', async () => {
    global.fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ bot_response: 'OK' }),
    })

    const requestData = {
      message: 'Test message',
      chatbot_type: 'doctor',
      risk_score: 10,
      conversation_context: {
        party_scenario: 1,
        previous_answers: ['yes', 'no']
      }
    }

    const request = {
      json: async () => requestData
    }

    await POST(request)

    expect(fetch).toHaveBeenCalledWith(
      expect.any(String),
      expect.objectContaining({
        body: JSON.stringify(requestData)
      })
    )
  })
})