import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '../services/analytics.service';
import { useDashboard } from '../context/DashboardContext';
import { useMemo } from 'react';

// Reusable hook for fetching KPIs
export function useKpis(datasetId: string) {
  return useQuery({
    queryKey: ['kpis', datasetId],
    queryFn: () => analyticsService.getKPIs(datasetId),
    enabled: !!datasetId,
  });
}

// Reusable hook for fetching Metrics by category
export function useMetrics(datasetId: string, category: string) {
  const { filters } = useDashboard();
  
  return useQuery({
    queryKey: ['metrics', datasetId, category, filters],
    queryFn: () => analyticsService.getMetrics(datasetId, category),
    enabled: !!datasetId,
    // Typically you would pass filters to backend here, but we are doing frontend filtering for MVP where backend doesn't support it yet
  });
}

export function useSegments(datasetId: string) {
  return useQuery({
    queryKey: ['segments', datasetId],
    queryFn: () => analyticsService.getSegments(datasetId),
    enabled: !!datasetId,
  });
}

// Helper to convert backend object { "2023-01-01": 100, "2023-01-02": 200 } to Recharts [{name: "2023-01-01", value: 100}]
export function useChartData(metricValue: any) {
  return useMemo(() => {
    if (!metricValue || typeof metricValue !== 'object' || Array.isArray(metricValue)) {
      return [];
    }
    
    return Object.entries(metricValue).map(([key, value]) => ({
      name: key,
      value: typeof value === 'number' ? Number(value.toFixed(2)) : value,
    }));
  }, [metricValue]);
}
