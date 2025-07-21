/**
 * Integration tests for Frontend-Backend communication
 * These tests verify the complete flow from UI to backend API
 */

import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatBox from './app/[role]/page'
import { POST as chatHandler } from './app/api/chat/route'

// Mock useParams
jest.mock('next/navigation', () => ({
  useParams: jest.fn(() => ({ role: 'ai' }))
}))

// Mock global fetch
global.fetch = jest.fn()

describe('Frontend-Backend Integration Tests', () => {
  beforeEach(() => {
    fetch.mockClear()
    process.env.BACKEND_API_URL = 'http://localhost:8080'
    process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8080'
  })

  describe('Assessment Flow', () => {
    test('loads and displays assessment questions on mount', async () => {
      // Mock assessment API response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'How old are you?',
          options: [
            { text: 'Under 18', next: '1', score: 0 },
            { text: '18-20', next: '2', score: 1 },
            { text: '21 or older', next: '3', score: 2 }
          ]
        })
      })

      render(<ChatBox params={{ role: 'ai' }} />)
      
      // Should initially show loading
      expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
      
      // Wait for assessment to load
      await waitFor(() => {
        expect(screen.getByText('How old are you?')).toBeInTheDocument()
        expect(screen.getByText('Under 18')).toBeInTheDocument()
        expect(screen.getByText('18-20')).toBeInTheDocument()
        expect(screen.getByText('21 or older')).toBeInTheDocument()
      })

      // Verify API was called correctly
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/api/get_assessment_step',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ stepKey: '0' })
        })
      )
    })

    test('progresses through assessment when answer is clicked', async () => {
      // First assessment step
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'How old are you?',
          options: [
            { text: 'Under 18', next: '1', score: 0 },
            { text: '18-20', next: '2', score: 1 },
            { text: '21 or older', next: '3', score: 2 }
          ]
        })
      })

      render(<ChatBox params={{ role: 'ai' }} />)
      
      await waitFor(() => {
        expect(screen.getByText('18-20')).toBeInTheDocument()
      })

      // Mock second assessment step
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Have you ever consumed alcohol?',
          options: [
            { text: 'Yes', next: 'result', score: 3 },
            { text: 'No', next: 'result', score: 0 }
          ]
        })
      })

      // Click an answer
      fireEvent.click(screen.getByText('18-20'))

      // Should load next question
      await waitFor(() => {
        expect(screen.getByText('Have you ever consumed alcohol?')).toBeInTheDocument()
      })

      // Verify second API call
      expect(fetch).toHaveBeenCalledTimes(2)
      expect(fetch).toHaveBeenLastCalledWith(
        'http://localhost:8080/api/get_assessment_step',
        expect.objectContaining({
          body: JSON.stringify({ stepKey: '2' })
        })
      )
    })
  })

  describe('Error Handling', () => {
    test('handles assessment API errors gracefully', async () => {
      // Mock API failure
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      const consoleSpy = jest.spyOn(console, 'error').mockImplementation()

      render(<ChatBox params={{ role: 'doctor' }} />)

      // Should still show loading message
      await waitFor(() => {
        expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
      })

      // Verify error was logged
      expect(consoleSpy).toHaveBeenCalledWith(
        'Error fetching assessment data:',
        expect.any(Error)
      )

      consoleSpy.mockRestore()
    })
  })

  describe('Chat Route Handler', () => {
    test('proxies requests to backend correctly', async () => {
      const mockBackendResponse = {
        bot_response: 'Hello from backend!',
        session_id: 'test-123'
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockBackendResponse,
      })

      const request = {
        json: async () => ({
          message: 'Hello',
          chatbot_type: 'ai',
          risk_score: 5,
          conversation_context: {}
        })
      }

      const response = await chatHandler(request)
      const data = await response.json()

      expect(data).toEqual(mockBackendResponse)
      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8080/',
        expect.objectContaining({
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            message: 'Hello',
            chatbot_type: 'ai',
            risk_score: 5,
            conversation_context: {}
          })
        })
      )
    })
  })
})