import '@testing-library/jest-dom'
import { beforeEach, vi } from 'vitest'

// Mock global variables
Object.defineProperty(globalThis, '__BACKEND_URL__', {
  value: 'http://localhost:8000',
  writable: true
})

// Setup global fetch mock
const mockFetch = vi.fn()
global.fetch = mockFetch

// Setup for each test
beforeEach(() => {
  vi.clearAllMocks()
  mockFetch.mockClear()
})

// Export mockFetch for use in tests
export { mockFetch }