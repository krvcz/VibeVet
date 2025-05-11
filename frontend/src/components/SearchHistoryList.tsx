import React from 'react';
import { useSearchHistory } from '../context/SearchHistoryContext';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import Button from './ui/Button';
import { Card, CardContent } from './ui/Card';
import { formatDistanceToNow } from '../utils/date';

interface SearchHistoryListProps {
  limit?: number;
}

const ITEMS_PER_PAGE = 20;

const SearchHistoryList: React.FC<SearchHistoryListProps> = ({ limit }) => {
  const { 
    history, 
    isLoading,
    pagination,
    currentPage,
    loadHistory
  } = useSearchHistory();

  const handlePageChange = (newPage: number) => {
    loadHistory(newPage);
  };

  const totalPages = Math.ceil(pagination.count / ITEMS_PER_PAGE);
  
  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (history.length === 0) {
    return <p className="text-gray-500 text-center py-6">Brak historii wyszukiwania.</p>;
  }
  
  let displayedHistory = history;
  if (limit && limit > 0) {
    displayedHistory = history.slice(0, limit);
  }
  
  return (
    <div>
      <div className="space-y-4">
        {displayedHistory.map(item => (
          <Card key={item.id}>
            <CardContent className="p-4">
              <div className="flex justify-between items-start mb-2">
                <h4 className="font-medium">{item.module}</h4>
                <span className="text-sm text-gray-500">
                  {formatDistanceToNow(new Date(item.timestamp))}
                </span>
              </div>
              <p className="text-sm text-gray-700">{item.query}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      
      {!limit && pagination.count > ITEMS_PER_PAGE && (
        <div className="mt-6 px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
          <div className="flex-1 flex justify-between sm:hidden">
            <Button
              variant="outline"
              onClick={() => handlePageChange(currentPage - 1)}
              disabled={!pagination.previous}
            >
              Poprzednia
            </Button>
            <Button
              variant="outline"
              onClick={() => handlePageChange(currentPage + 1)}
              disabled={!pagination.next}
            >
              Następna
            </Button>
          </div>
          
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-gray-700">
                Pokazuje <span className="font-medium">{((currentPage - 1) * ITEMS_PER_PAGE) + 1}</span>-
                <span className="font-medium">
                  {Math.min(currentPage * ITEMS_PER_PAGE, pagination.count)}
                </span> z{' '}
                <span className="font-medium">{pagination.count}</span> wyników
              </p>
            </div>
            
            <div className="flex space-x-2">
              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage - 1)}
                disabled={!pagination.previous}
                leftIcon={<ChevronLeft className="h-4 w-4" />}
              >
                Poprzednia
              </Button>
              
              <div className="flex items-center space-x-2">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => (
                  <Button
                    key={page}
                    variant={page === currentPage ? 'primary' : 'outline'}
                    size="sm"
                    onClick={() => handlePageChange(page)}
                  >
                    {page}
                  </Button>
                ))}
              </div>
              
              <Button
                variant="outline"
                size="sm"
                onClick={() => handlePageChange(currentPage + 1)}
                disabled={!pagination.next}
                rightIcon={<ChevronRight className="h-4 w-4" />}
              >
                Następna
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SearchHistoryList;