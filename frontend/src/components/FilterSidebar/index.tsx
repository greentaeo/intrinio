// src/components/FilterSidebar/index.tsx
import { useCallback } from 'react';
import { Card, Title, Button, Text } from '@tremor/react';
import { Filter } from './Filter';
import { CategoryFilters, FilterValue } from './types';
import { METRICS_BY_CATEGORY } from './constants';
import { useScreenerStore } from '../../store/screenerStore';
import { useScreenerData } from '../../hooks/useScreenerData';

interface FilterSidebarProps {
  onFilterChange: (filters: Record<string, any>) => void;
}

const FilterSidebar: React.FC<FilterSidebarProps> = ({ onFilterChange }) => {
  const setFilters = useScreenerStore((state) => state.setFilters);
  const { filters } = useScreenerStore();
  const { isLoading, refetch } = useScreenerData(filters);

  // 필터 변경 핸들러
  const handleFilterChange = useCallback((category: string, metricId: string, value: FilterValue) => {
    console.log('Filter Change:', { category, metricId, value }); // 디버깅
    
    setFilters((prev: CategoryFilters) => {
      const newFilters = { ...prev };
      
      if (!newFilters[category]) {
        newFilters[category] = {};
      }

      // select 타입인 경우
      if (value.operator && value.value !== undefined) {
        newFilters[category][metricId] = {
          operator: value.operator,
          value: value.value
        };
      }
      // number 타입인 경우
      else if (value.min !== null || value.max !== null) {
        newFilters[category][metricId] = {
          min: value.min,
          max: value.max
        };
      }
      // 초기화인 경우
      else {
        delete newFilters[category][metricId];
        if (Object.keys(newFilters[category]).length === 0) {
          delete newFilters[category];
        }
      }

      console.log('New Filters:', newFilters); // 디버깅
      return newFilters;
    });
  }, [setFilters]);

  // 필터 초기화
  const handleResetAll = useCallback(() => {
    setFilters({});
  }, [setFilters]);

  // 필터 제거
  const handleRemoveActiveFilter = (category: string, metricId: string) => {
    setFilters(prev => {
      const newFilters = { ...prev } as CategoryFilters;
      if (newFilters[category]) {
        delete newFilters[category][metricId];
        if (Object.keys(newFilters[category]).length === 0) {
          delete newFilters[category];
        }
      }
      return newFilters;
    });
  };

  // 1. 카테고리별 적용
  const handleApplyCategoryFilters = useCallback(async (category: string) => {
    try {
      if (!(category in filters)) return;
      await refetch();
      onFilterChange(filters);
    } catch (error) {
      console.error('카테고리 필터 적용 중 류:', error);
    }
  }, [filters, refetch, onFilterChange]);

  // 2. 전체 필터 적용
  const handleApplyFilters = useCallback(async () => {
    try {
      if (Object.keys(filters).length === 0) {
        console.log('적용할 필터가 없습니다');
        return;
      }
      await refetch();
      onFilterChange(filters);
    } catch (error) {
      console.error('필터 적용 중 오류:', error);
    }
  }, [filters, refetch, onFilterChange]);

  return (
    <div className="w-80 h-full bg-[#252B3D] p-4 overflow-y-auto">
      <div className="flex justify-between items-center mb-6">
        <Title className="text-xl font-bold text-white">필터</Title>
      </div>

      {Object.entries(METRICS_BY_CATEGORY).map(([category, metrics]) => (
        <Card key={category} className="mb-4 bg-[#1E2330]">
          <div className="flex justify-between items-center mb-4">
            <Title className="text-white">{category}</Title>
            <div className="flex gap-2">
              <Button
                size="xs"
                variant="secondary"
                onClick={() => handleApplyCategoryFilters(category)}
                className="text-purple-400 hover:text-purple-300 bg-transparent border border-purple-400"
              >
                적용
              </Button>
            </div>
          </div>
          {metrics.map((metric) => (
            <div key={metric.key} className="mb-4">
              <Text className="text-white mb-2">{metric.kr}</Text>
              <Filter
                value={{
                  metric: {
                    ...metric,
                    inputType: metric.inputType || "number",
                  },
                  currentValue: filters[category]?.[metric.key] || 
                    (metric.inputType === 'select' ? { operator: 'gte', value: null } : { min: null, max: null })
                }}
                onChange={(value) => handleFilterChange(category, metric.key, value)}
              />
            </div>
          ))}
        </Card>
      ))}
    </div>
  );
};

export default FilterSidebar;