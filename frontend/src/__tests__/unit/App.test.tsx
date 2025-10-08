import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../../App'

// Mock fetch
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('App Component', () => {
  beforeEach(() => {
    mockFetch.mockClear()
  })

  it('renders the main heading', () => {
    render(<App />)
    expect(screen.getByText('Legal Easy')).toBeInTheDocument()
  })

  it('renders the description text', () => {
    render(<App />)
    expect(screen.getByText(/Click the button to fetch a random number/)).toBeInTheDocument()
  })

  it('renders the get random number button', () => {
    render(<App />)
    expect(screen.getByRole('button', { name: /Get Random Number/i })).toBeInTheDocument()
  })

  it('displays initial state correctly', () => {
    render(<App />)
    expect(screen.getByText('—')).toBeInTheDocument()
    expect(screen.getByText('Backend: http://localhost:8000')).toBeInTheDocument()
  })

  it('shows loading state when button is clicked', async () => {
    mockFetch.mockImplementation(() => new Promise(() => {})) // Never resolves
    
    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    expect(screen.getByText('Loading...')).toBeInTheDocument()
    expect(button).toBeDisabled()
  })

  it('displays random number on successful API call', async () => {
    const mockResponse = { value: 42 }
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    await waitFor(() => {
      expect(screen.getByText('42')).toBeInTheDocument()
    })
    
    expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/random')
  })

  it('displays error message on API failure', async () => {
    mockFetch.mockRejectedValueOnce(new Error('Network error'))

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    await waitFor(() => {
      expect(screen.getByText('Error: Network error')).toBeInTheDocument()
    })
  })

  it('displays error message on HTTP error response', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: false,
      status: 500
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    await waitFor(() => {
      expect(screen.getByText('Error: HTTP 500')).toBeInTheDocument()
    })
  })

  it('re-enables button after API call completes', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ value: 42 })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    await waitFor(() => {
      expect(button).not.toBeDisabled()
    })
  })

  it('clears previous error when making new request', async () => {
    // First call fails
    mockFetch.mockRejectedValueOnce(new Error('Network error'))
    
    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })
    
    await act(async () => {
      await userEvent.click(button)
    })
    await waitFor(() => {
      expect(screen.getByText('Error: Network error')).toBeInTheDocument()
    })

    // Second call succeeds
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ value: 42 })
    })
    
    await act(async () => {
      await userEvent.click(button)
    })
    
    await waitFor(() => {
      expect(screen.getByText('42')).toBeInTheDocument()
      expect(screen.queryByText('Error: Network error')).not.toBeInTheDocument()
    })
  })
})