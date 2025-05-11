import React from 'react';
import { cn } from '../../utils/cn';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  interactive?: boolean;
}

export const Card: React.FC<CardProps> = ({ 
  children, 
  className, 
  interactive = false,
  ...props 
}) => {
  return (
    <div 
      className={cn(
        'bg-card text-card-foreground rounded-lg border shadow-sm',
        interactive && 'card-hover',
        className
      )} 
      {...props}
    >
      {children}
    </div>
  );
};

interface CardHeaderProps {
  children: React.ReactNode;
  className?: string;
}

export const CardHeader: React.FC<CardHeaderProps> = ({ 
  children, 
  className, 
  ...props 
}) => {
  return (
    <div 
      className={cn('flex flex-col space-y-1.5 p-6', className)} 
      {...props}
    >
      {children}
    </div>
  );
};

interface CardTitleProps {
  children: React.ReactNode;
  className?: string;
  as?: React.ElementType;
}

export const CardTitle: React.FC<CardTitleProps> = ({ 
  children, 
  className, 
  as: Component = 'h3', 
  ...props 
}) => {
  return (
    <Component 
      className={cn('text-2xl font-semibold leading-none tracking-tight', className)} 
      {...props}
    >
      {children}
    </Component>
  );
};

interface CardDescriptionProps {
  children: React.ReactNode;
  className?: string;
}

export const CardDescription: React.FC<CardDescriptionProps> = ({ 
  children, 
  className, 
  ...props 
}) => {
  return (
    <p 
      className={cn('text-sm text-muted-foreground', className)} 
      {...props}
    >
      {children}
    </p>
  );
};

interface CardContentProps {
  children: React.ReactNode;
  className?: string;
}

export const CardContent: React.FC<CardContentProps> = ({ 
  children, 
  className, 
  ...props 
}) => {
  return (
    <div 
      className={cn('p-6 pt-0', className)} 
      {...props}
    >
      {children}
    </div>
  );
};

interface CardFooterProps {
  children: React.ReactNode;
  className?: string;
}

export const CardFooter: React.FC<CardFooterProps> = ({ 
  children, 
  className, 
  ...props 
}) => {
  return (
    <div 
      className={cn('flex items-center p-6 pt-0', className)} 
      {...props}
    >
      {children}
    </div>
  );
};