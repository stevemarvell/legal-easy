import React from 'react';
import './Button.css';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
  children: React.ReactNode;
}

const Button = ({ 
  variant = 'primary', 
  size = 'medium', 
  loading = false, 
  children, 
  disabled,
  className = '',
  ...props 
}: ButtonProps) => {
  const buttonClass = `btn btn-${variant} btn-${size} ${loading ? 'loading' : ''} ${className}`.trim();

  return (
    <button 
      className={buttonClass}
      disabled={disabled || loading}
      {...props}
    >
      {loading ? (
        <>
          <span className="btn-spinner"></span>
          Loading...
        </>
      ) : (
        children
      )}
    </button>
  );
};

export default Button;