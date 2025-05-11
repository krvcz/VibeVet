import React from 'react';
import { formatDistanceToNow } from '../utils/date';
import { Clock, BookOpen, Pill, Activity } from 'lucide-react';
import { Card, CardContent, CardHeader } from './ui/Card';
import FeedbackButtons from './FeedbackButtons';
import { HistoryItem as HistoryItemType } from '../context/SearchHistoryContext';
import { useSearchHistory } from '../context/SearchHistoryContext';

interface HistoryItemProps {
  item: HistoryItemType;
}

const HistoryItem: React.FC<HistoryItemProps> = ({ item }) => {
  const { rateHistoryItem } = useSearchHistory();
  
  // Get icon based on history item type
  const getIcon = () => {
    switch (item.type) {
      case 'dosage':
        return <Pill className="w-5 h-5 text-primary" />;
      case 'interaction':
        return <Activity className="w-5 h-5 text-secondary" />;
      case 'treatment':
        return <BookOpen className="w-5 h-5 text-accent" />;
      default:
        return null;
    }
  };
  
  // Get title based on history item type
  const getTitle = () => {
    switch (item.type) {
      case 'dosage':
        return 'Obliczenie Dawki';
      case 'interaction':
        return 'Interakcja Leków';
      case 'treatment':
        return 'Poradnik Leczenia';
      default:
        return 'Wyszukiwanie';
    }
  };
  
  const handleFeedback = (feedback: 'up' | 'down') => {
    rateHistoryItem(item.id, feedback);
  };
  
  return (
    <Card className="w-full mb-4 overflow-hidden">
      <CardHeader className="bg-gray-50 pb-3 flex flex-row items-center justify-between">
        <div className="flex items-center space-x-2">
          {getIcon()}
          <h4 className="font-medium">{getTitle()}</h4>
        </div>
        <div className="flex items-center text-sm text-gray-500">
          <Clock className="w-3 h-3 mr-1" />
          <span>{formatDistanceToNow(new Date(item.timestamp))}</span>
        </div>
      </CardHeader>
      <CardContent className="p-4">
        <div className="mb-3">
          <h5 className="text-sm font-medium text-gray-500 mb-1">Zapytanie</h5>
          <p className="text-sm">{item.query}</p>
        </div>
        
        <div className="mb-3">
          <h5 className="text-sm font-medium text-gray-500 mb-1">Wynik</h5>
          <p className="text-sm">{item.result}</p>
        </div>
        
        <div className="flex justify-end">
          <FeedbackButtons 
            onFeedback={handleFeedback}
            initialValue={item.rating}
            size="sm"
          />
        </div>
      </CardContent>
    </Card>
  );
};

export default HistoryItem;