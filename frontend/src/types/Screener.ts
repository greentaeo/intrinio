// 스크리너 관련 타입 정의
export interface ScreenerItem {
  symbol: string;
  companyName: string;
  // 필요한 다른 필드들 추가
}

export type Operator = 'gt' | 'lt' | 'gte' | 'lte' | 'eq' | 'between';

export interface ScreenerCriteria {
  [key: string]: [Operator, number];
}

export interface ScreenerRequest {
  criteria: ScreenerCriteria;
  page?: number;
  limit?: number;
  sort_by?: string;
  order?: 'asc' | 'desc';
}

export interface ScreenerResponse {
  status: string;
  pagination: {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
  };
  sort: {
    field: string;
    order: string;
  } | null;
  data: Array<{
    id: string;
    ticker: string;
    name: string;
    exchange: string;
    [key: string]: any;
  }>;
  metadata: {
    timestamp: string;
    filters_applied: ScreenerCriteria;
  };
}

// 카테고리 타입 정의
export interface CategoryFilters {
  growth: { [key: string]: FilterValue };
  profitability: { [key: string]: FilterValue };
  financialStability: { [key: string]: FilterValue };
  valuation: { [key: string]: FilterValue };
  cashFlow: { [key: string]: FilterValue };
}

export type FilterType = CategoryFilters;

interface FilterValue {
  min?: number | null;
  max?: number | null;
}

export interface ScreenerFilters {
  [category: string]: {
    [metricId: string]: FilterValue;
  };
}
