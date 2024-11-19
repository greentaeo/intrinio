// src/services/api.ts
import axios from 'axios';

// 기본 URL 설정
const api = axios.create({
  baseURL: 'http://localhost:8000/api/screener',  // 경로 수정
  headers: {
    'Content-Type': 'application/json',
  }
});

export const screenerApi = {
  fetchScreenerData: async (filters: ScreenerFilters) => {
    try {
      // 유효한 필터값만 전송
      const cleanedFilters = Object.entries(filters).reduce((acc, [category, metrics]) => {
        const validMetrics = Object.entries(metrics).reduce((metricAcc, [metricId, value]) => {
          if (value.min !== null || value.max !== null) {
            metricAcc[metricId] = {
              min: value.min !== null ? Number(value.min) : null,
              max: value.max !== null ? Number(value.max) : null
            };
          }
          return metricAcc;
        }, {});

        if (Object.keys(validMetrics).length > 0) {
          acc[category] = validMetrics;
        }
        return acc;
      }, {});

      // 필터가 비어있으면 기본 데이터 요청
      if (Object.keys(cleanedFilters).length === 0) {
        const response = await api.get('');
        return response.data;
      }

      // 필터가 있으면 POST 요청
      const response = await api.post('/filter', cleanedFilters);
      return response.data;
    } catch (error) {
      console.error('Screener API Error:', error);
      if (axios.isAxiosError(error)) {
        console.error('Request data:', JSON.stringify(error.config?.data));
        console.error('Response data:', error.response?.data);
      }
      throw error;
    }
  }
};

