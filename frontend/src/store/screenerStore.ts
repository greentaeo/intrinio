import { create } from 'zustand';
import { FilterValue } from '../components/FilterSidebar/types';

interface CategoryFilters {
  [category: string]: {
    [metricId: string]: {
      min?: number | null;
      max?: number | null;
      operator?: string;
      value?: any;
    };
  };
}

interface ScreenerState {
  filters: CategoryFilters;
  setFilters: (
    filters: CategoryFilters | ((prev: CategoryFilters) => CategoryFilters)
  ) => void;
  resetFilters: () => void;
}

export const useScreenerStore = create<ScreenerState>((set) => ({
  filters: {},
  setFilters: (filters) => set((state) => ({ 
    filters: typeof filters === 'function' ? filters(state.filters) : filters 
  })),
  resetFilters: () => set({ filters: {} })
})); 