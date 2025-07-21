import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import ChooseAvatar from './ChooseAvatar'

// Import the mocked useRouter
const { useRouter } = require('next/navigation')

describe('ChooseAvatar Component', () => {
  let mockPush

  beforeEach(() => {
    mockPush = jest.fn()
    useRouter.mockImplementation(() => ({
      push: mockPush,
      replace: jest.fn(),
      prefetch: jest.fn(),
      back: jest.fn(),
      pathname: '/',
      route: '/',
      asPath: '/',
      query: {},
    }))
    // Reset Math.random to be predictable in tests
    jest.spyOn(Math, 'random')
  })

  afterEach(() => {
    jest.restoreAllMocks()
  })

  test('renders loading text', () => {
    render(<ChooseAvatar />)
    expect(screen.getByText('Redirecting...')).toBeInTheDocument()
  })

  test('redirects to ai role when random is 0', async () => {
    Math.random.mockReturnValue(0)
    render(<ChooseAvatar />)
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/ai')
    })
  })

  test('redirects to doctor role when random is 0.4', async () => {
    Math.random.mockReturnValue(0.4)
    render(<ChooseAvatar />)
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/doctor')
    })
  })

  test('redirects to student role when random is 0.8', async () => {
    Math.random.mockReturnValue(0.8)
    render(<ChooseAvatar />)
    
    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith('/student')
    })
  })

  test('mounts and unmounts without errors', () => {
    const { unmount } = render(<ChooseAvatar />)
    expect(() => unmount()).not.toThrow()
  })

  test('triggers redirect on component mount', () => {
    render(<ChooseAvatar />)
    // Should redirect immediately
    expect(mockPush).toHaveBeenCalledTimes(1)
  })
})