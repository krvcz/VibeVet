import React from 'react';
import { cn } from '../../utils/cn';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, label, error, fullWidth = false, leftIcon, rightIcon, ...props }, ref) => {
    return (
      <div className={cn('flex flex-col space-y-2', fullWidth && 'w-full')}>
        {label && (
          <label
            className="text-sm font-medium text-gray-700"
            htmlFor={props.id || props.name}
          >
            {label}
          </label>
        )}

        <div className="relative">
          {leftIcon && (
            <div className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500">
              {leftIcon}
            </div>
          )}

          <input
            type={type}
            className={cn(
              'flex h-10 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 input-focus-animation',
              error && 'border-error focus-visible:ring-error',
              leftIcon && 'pl-10',
              rightIcon && 'pr-10',
              fullWidth && 'w-full',
              className
            )}
            ref={ref}
            {...props}
          />

          {rightIcon && (
            <div className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500">
              {rightIcon}
            </div>
          )}
        </div>

        {error && <p className="text-sm text-error">{error}</p>}
      </div>
    );
  }
);

Input.displayName = 'Input';
export default Input;