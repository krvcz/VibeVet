import React from 'react';
import { cn } from '../../utils/cn';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'link' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ 
    children, 
    className, 
    variant = 'primary', 
    size = 'md', 
    isLoading = false, 
    fullWidth = false,
    leftIcon,
    rightIcon,
    disabled,
    ...props 
  }, ref) => {
    // Base styles that apply to all buttons
    const baseStyles = 'inline-flex items-center justify-center rounded-md font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none btn-click-effect';
    
    // Size variations
    const sizeStyles = {
      sm: 'h-8 px-3 text-xs',
      md: 'h-10 px-4 text-sm',
      lg: 'h-12 px-8 text-base'
    };
    
    // Variant styles
    const variantStyles = {
      primary: 'bg-primary text-primary-foreground hover:bg-primary/90 focus:ring-primary',
      secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/90 focus:ring-secondary',
      outline: 'border border-input bg-transparent hover:bg-muted hover:text-foreground focus:ring-primary',
      ghost: 'hover:bg-muted hover:text-foreground focus:ring-primary',
      link: 'text-primary underline-offset-4 hover:underline focus:ring-primary',
      success: 'bg-success text-success-foreground hover:bg-success/90 focus:ring-success',
      danger: 'bg-error text-error-foreground hover:bg-error/90 focus:ring-error'
    };
    
    // Width styles
    const widthStyles = fullWidth ? 'w-full' : '';
    
    // Loading state
    const loadingElement = isLoading ? (
      <span className="mr-2">
        <svg className="animate-spin h-4 w-4 text-current" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
      </span>
    ) : null;
    
    return (
      <button
        ref={ref}
        className={cn(
          baseStyles,
          sizeStyles[size],
          variantStyles[variant],
          widthStyles,
          className
        )}
        disabled={disabled || isLoading}
        {...props}
      >
        {isLoading && loadingElement}
        {!isLoading && leftIcon && <span className="mr-2">{leftIcon}</span>}
        {children}
        {!isLoading && rightIcon && <span className="ml-2">{rightIcon}</span>}
      </button>
    );
  }
);

Button.displayName = 'Button';
export default Button;