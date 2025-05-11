import React, { useState } from 'react';
import { ThumbsUp, ThumbsDown } from 'lucide-react';
import { cn } from '../utils/cn';

interface FeedbackButtonsProps {
  onFeedback: (feedback: 'up' | 'down') => void;
  initialValue?: 'up' | 'down' | null;
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const FeedbackButtons: React.FC<FeedbackButtonsProps> = ({
  onFeedback,
  initialValue = null,
  size = 'md',
  className
}) => {
  const [feedback, setFeedback] = useState<'up' | 'down' | null>(initialValue);
  
  const handleFeedback = (value: 'up' | 'down') => {
    if (feedback === value) {
      // If clicking the same button again, clear the selection
      setFeedback(null);
      onFeedback(value); // Still send the feedback for toggling off
    } else {
      setFeedback(value);
      onFeedback(value);
    }
  };
  
  // Sizing based on the size prop
  const iconSizes = {
    sm: 'h-4 w-4',
    md: 'h-5 w-5',
    lg: 'h-6 w-6'
  };
  
  const buttonSizes = {
    sm: 'p-1',
    md: 'p-2',
    lg: 'p-3'
  };
  
  return (
    <div className={cn('flex items-center space-x-2', className)}>
      <button
        type="button"
        onClick={() => handleFeedback('up')}
        className={cn(
          'rounded-full transition-all duration-200',
          buttonSizes[size],
          feedback === 'up' 
            ? 'bg-success/10 text-success' 
            : 'bg-transparent text-gray-400 hover:bg-gray-100 hover:text-gray-600'
        )}
        aria-label="Pomocne"
      >
        <ThumbsUp className={cn(
          iconSizes[size],
          feedback === 'up' && 'animate-bounce'
        )} />
      </button>
      
      <button
        type="button"
        onClick={() => handleFeedback('down')}
        className={cn(
          'rounded-full transition-all duration-200',
          buttonSizes[size],
          feedback === 'down' 
            ? 'bg-error/10 text-error' 
            : 'bg-transparent text-gray-400 hover:bg-gray-100 hover:text-gray-600'
        )}
        aria-label="Niepomocne"
      >
        <ThumbsDown className={cn(
          iconSizes[size],
          feedback === 'down' && 'animate-bounce'
        )} />
      </button>
    </div>
  );
};

export default FeedbackButtons;