import { useState, useEffect } from 'react';
import FilterSidebar from '../FilterSidebar';
import ScreenerTable from '../ScreenerTable';
import { ActiveFilters } from '../ActiveFilters';
import { useScreenerData } from '../../hooks/useScreenerData';
import { useScreenerStore } from '../../store/screenerStore';
import Layout from '../Layout';

const Screener = () => {
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

  if (error) {
    return <div>에러 발생했습니다: {error.message}</div>;
  }

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
      <ScreenerTable 
        data={data?.data || []} 
        isLoading={isLoading} 
      />
    </Layout>
  );
};

export default Screener;
