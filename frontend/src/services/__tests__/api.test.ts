import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ApiClient } from '../api';
import { mockFetch } from '../../__mocks__/api';

// Mock fetch globally
const originalFetch = global.fetch;

describe('ApiClient', () => {
  let apiClient: ApiClient;

  beforeEach(() => {
    apiClient = new ApiClient('http://localhost:8000');
    global.fetch = vi.fn().mockImplementation(mockFetch);
  });

  afterEach(() => {
    global.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  describe('GET requests', () => {
    it('makes successful GET request', async () => {
      const response = await apiClient.get('/api/cases');
      
      expect(response.status).toBe(200);
      expect(response.data).toBeDefined();
      expect(Array.isArray(response.data)).toBe(true);
    });

    it('handles 404 errors', async () => {
      try {
        await apiClient.get('/api/nonexistent');
      } catch (error: any) {
        expect(error.name).toBe('ApiError');
        expect(error.status).toBe(404);
      }
    });
  });

  describe('POST requests', () => {
    it('makes successful POST request with data', async () => {
      const testData = { title: 'Test Case', description: 'Test Description' };
      
      // Mock a successful POST response
      global.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: () => Promise.resolve({ id: 'new-case', ...testData }),
      });

      const response = await apiClient.post('/api/cases', testData);
      
      expect(response.status).toBe(201);
      expect(response.data.title).toBe(testData.title);
    });
  });

  describe('Error handling', () => {
    it('handles network errors', async () => {
      global.fetch = vi.fn().mockRejectedValue(new Error('Network error'));

      try {
        await apiClient.get('/api/cases');
      } catch (error: any) {
        expect(error.name).toBe('ApiError');
        expect(error.message).toBe('Network error');
      }
    });

    it('handles JSON parsing errors', async () => {
      global.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: () => Promise.reject(new Error('Invalid JSON')),
      });

      try {
        await apiClient.get('/api/cases');
      } catch (error: any) {
        expect(error.name).toBe('ApiError');
        expect(error.status).toBe(500);
      }
    });
  });
});