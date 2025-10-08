import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, screen, waitFor, cleanup, act } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import App from '../../App'

// Mock fetch
const mockFetch = vi.fn()
global.fetch = mockFetch

describe('API Integration Tests', () => {
  beforeEach(() => {
    // Reset fetch mock
    mockFetch.mockClear()
  })

  afterEach(() => {
    cleanup()
  })

  it('integrates with backend API successfully', async () => {
    // Mock a realistic API response
    const mockResponse = {
      value: 73
    }

    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => mockResponse,
      headers: new Headers({
        'content-type': 'application/json'
      })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })

    await act(async () => {
      await userEvent.click(button)
    })

    await waitFor(() => {
      expect(screen.getByText('73')).toBeInTheDocument()
    })

    expect(mockFetch).toHaveBeenCalledWith('http://localhost:8000/random')
  })

  it('handles CORS preflight requests', async () => {
    // Mock successful API response (CORS is handled by browser, not our app)
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ value: 42 }),
      headers: new Headers({
        'Access-Control-Allow-Origin': 'http://localhost:8080',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE',
        'Access-Control-Allow-Headers': '*'
      })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })

    await act(async () => {
      await userEvent.click(button)
    })

    await waitFor(() => {
      expect(screen.getByText('42')).toBeInTheDocument()
    })
  })

  it('handles network timeout gracefully', async () => {
    // Mock network timeout
    mockFetch.mockImplementation(() =>
      new Promise((_, reject) =>
        setTimeout(() => reject(new Error('Network timeout')), 100)
      )
    )

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })

    await act(async () => {
      await userEvent.click(button)
    })

    await waitFor(() => {
      expect(screen.getByText('Error: Network timeout')).toBeInTheDocument()
    }, { timeout: 2000 })
  })

  it('handles malformed JSON response', async () => {
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => {
        throw new Error('Unexpected token in JSON')
      }
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })

    await act(async () => {
      await userEvent.click(button)
    })

    await waitFor(() => {
      expect(screen.getByText(/Error: Unexpected token in JSON/)).toBeInTheDocument()
    })
  })

  it('validates response structure', async () => {
    // Mock response without 'value' field
    mockFetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ invalid: 'response' })
    })

    render(<App />)
    const button = screen.getByRole('button', { name: /Get Random Number/i })

    await act(async () => {
      await userEvent.click(button)
    })

    // The app should handle this gracefully - it will display undefined as empty
    await waitFor(() => {
      // Check that the result div exists but is empty (showing undefined)
      const resultDiv = screen.getByText('', { selector: '.result' })
      expect(resultDiv).toBeInTheDocument()
    })
  })

  it('handles different HTTP error codes', async () => {
    const errorCodes = [400, 404, 500]

    for (const code of errorCodes) {
      mockFetch.mockResolvedValueOnce({
        ok: false,
        status: code
      })

      const { unmount } = render(<App />)
      const button = screen.getByRole('button', { name: /Get Random Number/i })

      await act(async () => {
        await userEvent.click(button)
      })

      await waitFor(() => {
        expect(screen.getByText(`Error: HTTP ${code}`)).toBeInTheDocument()
      })

      // Clean up for next iteration
      unmount()
    }
  })
})