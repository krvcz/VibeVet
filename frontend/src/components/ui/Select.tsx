import React, { forwardRef } from 'react';
import { cn } from '../../utils/cn';
import { ChevronDown } from 'lucide-react';

export interface SelectOption {
  value: string;
  label: string;
}

export interface SelectProps extends Omit<React.SelectHTMLAttributes<HTMLSelectElement>, 'onChange'> {
  options: SelectOption[];
  label?: string;
  error?: string;
  fullWidth?: boolean;
  onChange?: (value: string) => void;
}

const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ className, options, label, error, fullWidth = false, onChange, ...props }, ref) => {
    const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      if (onChange) {
        onChange(e.target.value);
      }
    };

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
          <select
            className={cn(
              'appearance-none flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50 input-focus-animation pr-10',
              error && 'border-error focus-visible:ring-error',
              className
            )}
            ref={ref}
            onChange={handleChange}
            {...props}
          >
            {options.map((option) => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
          <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-500 pointer-events-none" />
        </div>

        {error && <p className="text-sm text-error">{error}</p>}
      </div>
    );
  }
);

Select.displayName = 'Select';
export default Select;