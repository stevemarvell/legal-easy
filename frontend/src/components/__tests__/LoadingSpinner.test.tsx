import { describe, it, expect } from 'vitest';
import { render, screen } from '../../test-utils';
import LoadingSpinner from '../LoadingSpinner';

describe('LoadingSpinner Component', () => {
  it('renders with default props', () => {
    render(<LoadingSpinner />);
    
    const spinner = document.querySelector('.loading-spinner');
    expect(spinner).toBeInTheDocument();
    expect(spinner).toHaveClass('medium');
  });

  it('renders with different sizes', () => {
    const { rerender } = render(<LoadingSpinner size="small" />);
    expect(document.querySelector('.loading-spinner')).toHaveClass('small');

    rerender(<LoadingSpinner size="large" />);
    expect(document.querySelector('.loading-spinner')).toHaveClass('large');
  });

  it('displays message when provided', () => {
    const message = 'Loading data...';
    render(<LoadingSpinner message={message} />);
    
    expect(screen.getByText(message)).toBeInTheDocument();
  });

  it('does not display message when not provided', () => {
    render(<LoadingSpinner />);
    
    const messageElement = document.querySelector('.loading-message');
    expect(messageElement).not.toBeInTheDocument();
  });
});