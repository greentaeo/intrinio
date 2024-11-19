// Path: /frontend/src/components/FilterSidebar/types.ts

export type MetricKey = "revenuegrowth" | "netincomegrowth" | "epsgrowth" | /* ... 다른 키들 ... */ "ocftocapex";

export interface MetricType {
    key: string;
    label: string;
    tooltip: string;
    en: string;
    kr: string;
    inputType: 'number' | 'select';
    options?: Array<{
        value: string | number;
        label: string;
    }>;
}
  
  export interface CategoryType {
    id: string;
    name: string;
    metrics: MetricType[];
  }
  
  export interface FilterValue {
    min?: number | null;
    max?: number | null;
    operator?: 'gte' | 'lte' | 'eq';
    value?: number | null;
  }
  
  export interface FilterState {
    [key: string]: FilterValue;
  }
  
  export interface FilterProps {
    value: {
      metric: Metric;
      currentValue: FilterValue;
    };
    onChange: (value: FilterValue) => void;
  }
  
  export interface FilterSidebarProps {
    onFilterChange: (newFilters: object) => void;
  }
  
  export interface FilterCategory {
    name: string;
    key: string;
    type?: 'select' | 'range';
    metrics: Metric[];
  }
  
  export interface FilterMetric {
    key: string;
    label: string;
    englishLabel: string;
    tooltip: string;
    min?: number;
    max?: number;
  }
  
  export interface FilterValues {
    [key: string]: {
      min?: number;
      max?: number;
    };
  }
  
  export interface MetricOption {
    key: string;
    label: string;
    value: {
      operator: string;
      clauses: Array<{
        field: string;
        operator: string;
        value: string;
      }>;
      groups?: Array<any>;
    };
    tooltip: string;
  }
  
  export interface Metric {
    key: string;
    kr: string;
    en: string;
    englishLabel: string;
    tooltip: string;
    inputType: string;
    unit: string;
    options?: Array<{ key: string; label: string }>;
  }

  export interface FilterRequest {
    [category: string]: CategoryFilters;
  }

  export interface MetricItem {
    key: string;
    kr: string;
    inputType: string;
    description?: string;
  }

  export type CategoryFilters = {
    [category: string]: {
      [metricId: string]: FilterValue;
    };
  };