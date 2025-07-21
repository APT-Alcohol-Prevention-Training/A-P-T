import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react'
import Home from './page'
import ChooseAvatar from './components/ChooseAvatar'

// Mock the ChooseAvatar component
jest.mock('./components/ChooseAvatar', () => {
  return jest.fn(() => <div>ChooseAvatar Component</div>)
})

describe('Home Page', () => {
  beforeEach(() => {
    ChooseAvatar.mockClear()
  })

  test('renders welcome message', () => {
    render(<Home />)
    expect(screen.getByText('Welcome to the')).toBeInTheDocument()
  })

  test('renders start button', () => {
    render(<Home />)
    // Button text includes special character, need to use partial matching
    expect(screen.getByRole('button')).toBeInTheDocument()
    expect(screen.getByRole('button')).toHaveTextContent('Get Started')
  })

  test('does not show ChooseAvatar initially', () => {
    render(<Home />)
    expect(screen.queryByText('ChooseAvatar Component')).not.toBeInTheDocument()
  })

  test('shows ChooseAvatar when start button is clicked', () => {
    render(<Home />)
    
    const startButton = screen.getByRole('button')
    fireEvent.click(startButton)
    
    expect(screen.getByText('ChooseAvatar Component')).toBeInTheDocument()
  })

  test('applies correct CSS classes', () => {
    const { container } = render(<Home />)
    
    // Check for main container classes
    const mainDiv = container.firstChild
    expect(mainDiv).toHaveClass('px-[32px]')
    expect(mainDiv).toHaveClass('md:px-[64px]')
    expect(mainDiv).toHaveClass('flex')
    expect(mainDiv).toHaveClass('flex-col')
    expect(mainDiv).toHaveClass('pt-[40px]')
    expect(mainDiv).toHaveClass('min-h-screen')
    expect(mainDiv).toHaveClass('bg-[#F6F6F2]')
  })

  test('renders logo images', () => {
    render(<Home />)
    
    const logos = screen.getAllByAltText('logo')
    expect(logos).toHaveLength(2) // logo3.svg and hands.svg both have alt="logo"
  })

  test('renders all images', () => {
    render(<Home />)
    
    // Check for all images in the component
    const images = screen.getAllByRole('img')
    expect(images).toHaveLength(3) // logo3.svg, arrow-right.svg, hands.svg
    
    // Check specific alt texts
    const logos = screen.getAllByAltText('logo')
    expect(logos).toHaveLength(2)
    expect(screen.getByAltText('arrow')).toBeInTheDocument()
  })

  test('button has correct styling classes', () => {
    render(<Home />)
    
    const button = screen.getByRole('button')
    expect(button).toHaveClass('bg-gradient-to-r')
    expect(button).toHaveClass('flex')
    expect(button).toHaveClass('items-center')
    expect(button).toHaveClass('rounded-[99px]')
  })

  test('component state changes when button is clicked', () => {
    render(<Home />)
    
    // Initially, ChooseAvatar should not be rendered
    expect(ChooseAvatar).not.toHaveBeenCalled()
    
    // Click the button
    fireEvent.click(screen.getByRole('button'))
    
    // ChooseAvatar should now be rendered
    expect(ChooseAvatar).toHaveBeenCalledTimes(1)
  })

  test('hides initial content when ChooseAvatar is shown', () => {
    render(<Home />)
    
    // Initially, welcome message should be visible
    expect(screen.getByText('Welcome to the')).toBeInTheDocument()
    
    // Click the button
    fireEvent.click(screen.getByRole('button'))
    
    // Welcome message should no longer be visible
    expect(screen.queryByText('Welcome to the')).not.toBeInTheDocument()
    expect(screen.getByText('ChooseAvatar Component')).toBeInTheDocument()
  })
})