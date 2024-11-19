import { useQuery } from '@tanstack/react-query';
import { screenerApi } from '../services/api';
import type { ScreenerFilters } from '../services/api';

export const useScreenerData = (filters: ScreenerFilters) => {
  return useQuery({
    queryKey: ['screenerData', filters],
    queryFn: () => screenerApi.fetchScreenerData(filters),
    enabled: Object.keys(filters).length > 0,
    retry: false
  });
};
