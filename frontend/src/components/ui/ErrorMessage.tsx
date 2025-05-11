import React from 'react';
import { AlertCircle } from 'lucide-react';
import { cn } from '../../utils/cn';

interface ErrorMessageProps {
  message: string;
  className?: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, className }) => {
  if (!message) return null;

  return (
    <div className={cn(
      'p-3 bg-error/10 border border-error rounded-md flex items-start gap-2',
      className
    )}>
      <AlertCircle className="w-5 h-5 text-error shrink-0 mt-0.5" />
      <p className="text-sm text-error">{message}</p>
    </div>
  );
};

export default ErrorMessage;