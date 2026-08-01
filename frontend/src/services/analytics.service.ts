import { api } from './api';

export interface AnalyticsJob {
    id: string;
    dataset_id: string;
    status: string;
    started_at: string;
    completed_at?: string;
    duration_ms?: number;
    summary?: any;
    analytics_version: string;
}

export interface KPIResult {
    id: string;
    kpi_name: string;
    kpi_category: string;
    value: number;
    previous_value?: number;
    percentage_change?: number;
    timestamp: string;
}

export interface AnalyticsMetric {
    id: string;
    metric_name: string;
    metric_category: string;
    dimension?: string;
    value: any;
    aggregation?: string;
    generated_at: string;
}

export interface CustomerSegment {
    id: string;
    segment_name: string;
    description?: string;
    customer_count: number;
    revenue?: number;
    percentage: number;
}

class AnalyticsService {
    async analyze(datasetId: string): Promise<AnalyticsJob> {
        const response = await api.post(`/datasets/${datasetId}/analyze`);
        return response.data;
    }

    async getStatus(datasetId: string): Promise<AnalyticsJob> {
        const response = await api.get(`/datasets/${datasetId}/status`);
        return response.data;
    }

    async getKPIs(datasetId: string): Promise<KPIResult[]> {
        const response = await api.get(`/datasets/${datasetId}/kpis`);
        return response.data;
    }

    async getMetrics(datasetId: string, category?: string): Promise<AnalyticsMetric[]> {
        const url = category ? `/datasets/${datasetId}/metrics?category=${category}` : `/datasets/${datasetId}/metrics`;
        const response = await api.get(url);
        return response.data;
    }

    async getSegments(datasetId: string): Promise<CustomerSegment[]> {
        const response = await api.get(`/datasets/${datasetId}/segments`);
        return response.data;
    }
}

export const analyticsService = new AnalyticsService();
