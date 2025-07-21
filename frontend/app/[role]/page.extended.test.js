import React from 'react'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatBox from './page'

// Mock useParams
const { useParams } = require('next/navigation')

// Mock fetch globally
global.fetch = jest.fn()

describe('ChatBox Component - Extended Tests', () => {
  beforeEach(() => {
    fetch.mockClear()
    useParams.mockReturnValue({ role: 'ai' })
  })

  describe('Assessment Answer Handling', () => {
    test('handles assessment answer selection correctly', async () => {
      // First step response
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

      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('18-20')).toBeInTheDocument()
      })

      // Second step response
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

      await waitFor(() => {
        expect(screen.getByText('Have you ever consumed alcohol?')).toBeInTheDocument()
      })
    })

    test('handles assessment completion', async () => {
      // Mock assessment step
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Final question',
          options: [
            { text: 'Yes', next: 'result', score: 5 },
            { text: 'No', next: 'result', score: 0 }
          ]
        })
      })

      // Mock training data fetch
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          moderate_risk: [
            {
              question: 'Training question 1',
              options: [
                { text: 'Option A', correct: true },
                { text: 'Option B', correct: false }
              ]
            }
          ]
        })
      })

      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Final question')).toBeInTheDocument()
      })

      // Click answer that leads to result
      fireEvent.click(screen.getByText('Yes'))

      // Should fetch training data after completion
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('/training_data.json')
      })
    })

    test('handles assessment end option', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Do you want to continue?',
          options: [
            { text: 'Yes', next: '2', score: 1 },
            { text: 'No, end assessment', end: true }
          ]
        })
      })

      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('No, end assessment')).toBeInTheDocument()
      })

      fireEvent.click(screen.getByText('No, end assessment'))

      // Should not make another API call
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(1)
      })
    })
  })

  describe('Chat Functionality After Assessment', () => {
    beforeEach(async () => {
      // Mock initial assessment
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Quick assessment',
          options: [
            { text: 'Complete', next: 'result', score: 5 }
          ]
        })
      })

      // Mock training data
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ low_risk: [] })
      })
    })

    test('sends chat message after assessment completion', async () => {
      render(<ChatBox />)
      
      // Complete assessment
      await waitFor(() => {
        expect(screen.getByText('Complete')).toBeInTheDocument()
      })
      
      fireEvent.click(screen.getByText('Complete'))

      // Wait for initial AI messages about party scenario
      await waitFor(() => {
        expect(screen.getByText(/Let's try a quick example together/)).toBeInTheDocument()
      }, { timeout: 3000 })

      // Wait for the party scenario message
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      // Mock chat response
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          bot_response: 'That\'s a great response!',
          session_id: 'test-session'
        })
      })

      const input = screen.getByPlaceholderText(/What do you want to share today?/)
      const sendButton = screen.getByRole('button', { name: 'send' })

      await userEvent.type(input, 'No thanks, I\'m good')
      fireEvent.click(sendButton)

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          '/api/chat',
          expect.objectContaining({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: expect.stringContaining('"message":"No thanks, I\'m good"')
          })
        )
      })
    })

    test('displays loading state while sending message', async () => {
      render(<ChatBox />)
      
      // Complete assessment quickly
      await waitFor(() => {
        expect(screen.getByText('Complete')).toBeInTheDocument()
      })
      
      fireEvent.click(screen.getByText('Complete'))

      // Wait for party scenario
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      // Delay response to test loading state
      global.fetch.mockImplementationOnce(() => 
        new Promise(resolve => setTimeout(() => resolve({
          ok: true,
          json: async () => ({ bot_response: 'Response' })
        }), 1000))
      )

      const input = screen.getByPlaceholderText(/What do you want to share today?/)
      const sendButton = screen.getByRole('button', { name: 'send' })

      await userEvent.type(input, 'Test')
      fireEvent.click(sendButton)

      // Check if loading state is shown (Loading... text appears)
      await waitFor(() => {
        expect(screen.getByText('Loading...')).toBeInTheDocument()
      })
    })
  })

  describe('Training Mode', () => {
    test('displays party scenario after assessment', async () => {
      // Quick assessment completion
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Assessment',
          options: [{ text: 'Done', next: 'result', score: 10 }]
        })
      })

      // Mock training data (though it's not directly used for display)
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          high_risk: []
        })
      })

      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Done')).toBeInTheDocument()
      })

      fireEvent.click(screen.getByText('Done'))

      // Wait for party scenario to appear
      await waitFor(() => {
        expect(screen.getByText(/Let's try a quick example together/)).toBeInTheDocument()
      }, { timeout: 3000 })

      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })
    })

    test('loads training data based on risk level', async () => {
      // Setup assessment with moderate risk score
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Assessment',
          options: [{ text: 'Done', next: 'result', score: 5 }]
        })
      })

      const mockTrainingData = {
        low_risk: [],
        moderate_risk: [
          {
            question: 'Training Q1',
            options: [
              { text: 'Correct', correct: true },
              { text: 'Wrong', correct: false }
            ]
          }
        ],
        high_risk: []
      }

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockTrainingData
      })

      render(<ChatBox />)
      
      // Complete assessment
      await waitFor(() => {
        expect(screen.getByText('Done')).toBeInTheDocument()
      })
      fireEvent.click(screen.getByText('Done'))

      // Verify training data was fetched
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith('/training_data.json')
      })

      // Even though training data is loaded, party scenario is shown
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })
    })
  })

  describe('Error Handling', () => {
    test('handles chat API errors gracefully', async () => {
      // Complete assessment first
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Assessment',
          options: [{ text: 'Done', next: 'result', score: 5 }]
        })
      })

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ moderate_risk: [] })
      })

      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Done')).toBeInTheDocument()
      })
      fireEvent.click(screen.getByText('Done'))

      // Wait for party scenario
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      // Mock error response
      global.fetch.mockResolvedValueOnce({
        ok: false,
        json: async () => ({ error: 'Server error' })
      })

      const input = screen.getByPlaceholderText(/What do you want to share today?/)
      await userEvent.type(input, 'Test')
      fireEvent.click(screen.getByRole('button', { name: 'send' }))

      // Should show error message
      await waitFor(() => {
        expect(screen.getByText(/Error: Server error/)).toBeInTheDocument()
      })
    })

    test('handles assessment API failure gracefully', async () => {
      // Mock console.error to avoid noise in test output
      const consoleError = jest.spyOn(console, 'error').mockImplementation()
      
      // First call fails
      global.fetch.mockRejectedValueOnce(new Error('Network error'))

      render(<ChatBox />)

      // Wait for error to be logged
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledTimes(1)
      })

      // Verify error was logged
      expect(consoleError).toHaveBeenCalledWith(
        'Error fetching assessment data:',
        expect.any(Error)
      )

      // Should show loading message since assessment failed
      expect(screen.getByText('Loading assessment questions...')).toBeInTheDocument()
      
      consoleError.mockRestore()
    })
  })

  describe('Input Validation', () => {
    beforeEach(async () => {
      // Setup to reach chat interface quickly
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          text: 'Quick',
          options: [{ text: 'Skip', next: 'result', score: 0 }]
        })
      })

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ low_risk: [] })
      })
    })

    test('prevents sending empty messages', async () => {
      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Skip')).toBeInTheDocument()
      })
      fireEvent.click(screen.getByText('Skip'))

      // Wait for party scenario
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      const sendButton = screen.getByRole('button', { name: 'send' })
      
      // Clear any previous fetch calls
      fetch.mockClear()
      
      // Try to send empty message
      fireEvent.click(sendButton)

      // Wait a bit to ensure no API call is made
      await new Promise(resolve => setTimeout(resolve, 100))

      // Should not call API for empty message
      expect(fetch).not.toHaveBeenCalled()
    })

    test('trims whitespace from messages', async () => {
      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Skip')).toBeInTheDocument()
      })
      fireEvent.click(screen.getByText('Skip'))

      // Wait for party scenario
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ bot_response: 'Response' })
      })

      const input = screen.getByPlaceholderText(/What do you want to share today?/)
      await userEvent.type(input, '   Hello   ')
      fireEvent.click(screen.getByRole('button', { name: 'send' }))

      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          '/api/chat',
          expect.objectContaining({
            body: expect.stringContaining('"message":"Hello"')
          })
        )
      })
    })

    test('handles scenario progression to second scenario', async () => {
      render(<ChatBox />)
      
      await waitFor(() => {
        expect(screen.getByText('Skip')).toBeInTheDocument()
      })
      fireEvent.click(screen.getByText('Skip'))

      // Wait for party scenario
      await waitFor(() => {
        expect(screen.getByText(/You're at a party/)).toBeInTheDocument()
      }, { timeout: 5000 })

      // Mock response that includes party_scenario context
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({ bot_response: 'Good choice!' })
      })

      const input = screen.getByPlaceholderText(/What do you want to share today?/)
      await userEvent.type(input, 'No thanks')
      fireEvent.click(screen.getByRole('button', { name: 'send' }))

      // Wait for second scenario message (should appear after 2 seconds)
      await waitFor(() => {
        expect(screen.getByText(/pre-game before the concert/)).toBeInTheDocument()
      }, { timeout: 5000 })
    })
  })
})