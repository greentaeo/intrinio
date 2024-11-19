import { useState } from 'react';
import Layout from '../../components/Layout';
import FilterSidebar from '../../components/FilterSidebar';
import ScreenerTable from '../../components/ScreenerTable';
import { useScreenerData } from '../../hooks/useScreenerData';
import { ActiveFilters } from '../../components/ActiveFilters';
import { useScreenerStore } from '../../store/screenerStore';

const ScreenerPage = () => {
  // Zustand store 사용
  const storeFilters = useScreenerStore((state) => state.filters);
  const setStoreFilters = useScreenerStore((state) => state.setFilters);
  const { data, isLoading, error } = useScreenerData(storeFilters);

  const handleFilterChange = (newFilters: Record<string, any>) => {
    setStoreFilters(newFilters);
  };

  const handleRemoveFilter = (category: string, metricId: string) => {
    setStoreFilters(prev => {
      const newFilters = { ...prev };
      if (newFilters[category]) {
        delete newFilters[category][metricId];
        if (Object.keys(newFilters[category]).length === 0) {
          delete newFilters[category];
        }
      }
      return newFilters;
    });
  };

  const handleResetFilters = () => {
    setStoreFilters({});
  };

  return (
    <Layout 
      sidebar={<FilterSidebar onFilterChange={handleFilterChange} />}
      activeFilters={
        <ActiveFilters
          filters={storeFilters}
          onRemove={handleRemoveFilter}
          onResetActive={handleResetFilters}
        />
      }
    >
      <div className="bg-[#1C2230] rounded-lg shadow-lg">
        <ScreenerTable 
          data={data?.data || []} 
          isLoading={isLoading} 
        />
        {error && (
          <div className="text-red-500 mt-4">
            에러가 발생했습니다: {error.message}
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ScreenerPage;