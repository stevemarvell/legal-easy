import React from 'react';
import { describe, it, expect } from 'vitest';
import { render, screen } from '../../../test-utils';

describe('Minimal Test', () => {
  it('should render a simple component', () => {
    render(<div data-testid="test">Hello World</div>);
    expect(screen.getByTestId('test')).toBeInTheDocument();
  });
});