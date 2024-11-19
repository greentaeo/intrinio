import { CategoryFilters } from '../FilterSidebar/types';

interface ActiveFiltersProps {
  filters: CategoryFilters;
  onRemove: (category: string, metricId: string) => void;
  onResetActive: () => void;
}

export const ActiveFilters: React.FC<ActiveFiltersProps> = ({
  filters,
  onRemove,
  onResetActive,
}) => {
  const hasActiveFilters = Object.keys(filters).length > 0;

  if (!hasActiveFilters) return null;

  return (
    <div className="p-4 bg-[#1E2330] rounded-lg mb-4">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-white text-lg">활성 필터</h3>
        <button
          onClick={onResetActive}
          className="text-xs text-gray-400 hover:text-gray-200"
        >
          모두 초기화
        </button>
      </div>
      <div className="flex flex-wrap gap-2">
        {Object.entries(filters).map(([category, categoryFilters]) => 
          Object.entries(categoryFilters).map(([metricId, values]) => {
            const hasValue = values.min !== null || values.max !== null || values.value !== undefined;
            if (!hasValue) return null;
            
            return (
              <div 
                key={`${category}-${metricId}`}
                className="inline-flex items-center bg-gray-700 rounded px-2 py-1"
              >
                <span className="text-gray-300 text-xs mr-1">{metricId}:</span>
                <span className="text-white text-xs">
                  {values.min !== null && `↑${values.min}`}
                  {values.min !== null && values.max !== null && ' | '}
                  {values.max !== null && `↓${values.max}`}
                  {values.value !== undefined && `${values.value}`}
                </span>
                <button
                  onClick={() => onRemove(category, metricId)}
                  className="ml-2 text-gray-400 hover:text-gray-200 text-xs"
                >
                  ×
                </button>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
