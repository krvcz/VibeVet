import React from 'react';
import { cn } from '../../utils/cn';

export interface TextareaProps extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  label?: string;
  error?: string;
  fullWidth?: boolean;
}

const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
  ({ className, label, error, fullWidth = false, ...props }, ref) => {
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

        <textarea
          className={cn(
            'flex min-h-[80px] rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 input-focus-animation',
            error && 'border-error focus-visible:ring-error',
            fullWidth && 'w-full',
            className
          )}
          ref={ref}
          {...props}
        />

        {error && <p className="text-sm text-error">{error}</p>}
      </div>
    );
  }
);

Textarea.displayName = 'Textarea';
export default Textarea;