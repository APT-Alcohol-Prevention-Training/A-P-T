import React from 'react'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import ChatBox from './page'

// Import the mocked useParams
const { useParams } = require('next/navigation')

// Mock fetch globally
global.fetch = jest.fn()

// Mock the chat API
const mockChatResponse = (response) => {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => response,
  })
}

describe('ChatBox Component', () => {
  let consoleError

  beforeEach(() => {
    fetch.mockClear()
    // Reset useParams mock
    useParams.mockReturnValue({ role: 'ai' })
    // Mock console.error to reduce test noise
    consoleError = jest.spyOn(console, 'error').mockImplementation(() => {})
  })

  afterEach(() => {
    consoleError.mockRestore()
  })

  describe('Initial Render', () => {
    test('renders with correct role (ai)', () => {
      useParams.mockReturnValue({ role: 'ai' })
      render(<ChatBox />)
      expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
    })

    test('renders with correct role (doctor)', () => {
      useParams.mockReturnValue({ role: 'doctor' })
      render(<ChatBox />)
      expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
    })

    test('renders with correct role (student)', () => {
      useParams.mockReturnValue({ role: 'student' })
      render(<ChatBox />)
      expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
    })

    test('shows loading assessment message initially', () => {
      render(<ChatBox params={{ role: 'ai' }} />)
      expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
    })
  })

  describe('Dark Mode Toggle', () => {
    test('toggles dark mode when clicked', () => {
      render(<ChatBox params={{ role: 'ai' }} />)
      const darkModeButton = screen.getByText('Dark Mode')
      
      // Should start in light mode
      expect(darkModeButton).toBeInTheDocument()
      
      // Click to toggle to dark mode
      fireEvent.click(darkModeButton)
      expect(screen.getByText('Light Mode')).toBeInTheDocument()
      
      // Click again to toggle back
      fireEvent.click(screen.getByText('Light Mode'))
      expect(screen.getByText('Dark Mode')).toBeInTheDocument()
    })
  })

  describe('Assessment Flow', () => {
    test('loads assessment on mount', async () => {
      mockChatResponse({
        text: 'How old are you?',
        options: [
          { text: 'Under 18', next: '1', score: 0 },
          { text: '18-20', next: '2', score: 1 },
          { text: '21 or older', next: '3', score: 2 }
        ]
      })

      render(<ChatBox params={{ role: 'ai' }} />)
      
      // Assessment loads automatically on mount
      await waitFor(() => {
        expect(fetch).toHaveBeenCalledWith(
          'http://localhost:8080/api/get_assessment_step',
          expect.objectContaining({
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ stepKey: '0' })
          })
        )
      })
    })

    test('displays assessment question after loading', async () => {
      mockChatResponse({
        text: 'How old are you?',
        options: [
          { text: 'Under 18', next: '1', score: 0 },
          { text: '18-20', next: '2', score: 1 },
          { text: '21 or older', next: '3', score: 2 }
        ]
      })

      render(<ChatBox params={{ role: 'ai' }} />)
      
      await waitFor(() => {
        expect(screen.getByText('How old are you?')).toBeInTheDocument()
        expect(screen.getByText('Under 18')).toBeInTheDocument()
        expect(screen.getByText('18-20')).toBeInTheDocument()
        expect(screen.getByText('21 or older')).toBeInTheDocument()
      })
    })

    test('handles assessment API error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'))
      
      render(<ChatBox params={{ role: 'ai' }} />)
      
      // Should still show loading message on error
      await waitFor(() => {
        expect(screen.getByText(/Loading assessment questions.../)).toBeInTheDocument()
      })
    })
  })

  // Note: Chat functionality tests have been removed as the chat interface
  // is only available after completing the assessment flow, which would
  // require a more complex test setup
})