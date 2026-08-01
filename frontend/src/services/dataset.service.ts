import { api } from './api';
import { Dataset, DatasetDetails, DatasetPreview } from '../types/dataset';

export const datasetService = {
  uploadDataset: async (file: File, displayName: string, description: string, onUploadProgress?: (progressEvent: any) => void) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('display_name', displayName);
    formData.append('description', description);

      const response = await api.post<Dataset>('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress
    });
    return response.data;
  },

  getDatasets: async (skip: number = 0, limit: number = 100, search?: string) => {
    const params = new URLSearchParams();
    params.append('skip', skip.toString());
    params.append('limit', limit.toString());
    if (search) params.append('search', search);

    const response = await api.get<Dataset[]>(`/datasets?${params.toString()}`);
    return response.data;
  },

  getDatasetDetails: async (id: string) => {
    const response = await api.get<DatasetDetails>(`/datasets/${id}`);
    return response.data;
  },

  getDatasetPreview: async (id: string, rows: number = 20) => {
    const response = await api.get<DatasetPreview>(`/datasets/${id}/preview?rows=${rows}`);
    return response.data;
  },

  deleteDataset: async (id: string) => {
    const response = await api.delete<{success: boolean, message: string}>(`/datasets/${id}`);
    return response.data;
  },

  triggerProfiling: async (id: string) => {
    const response = await api.post(`/datasets/${id}/profile`);
    return response.data;
  },

  getProfilingStatus: async (id: string) => {
    const response = await api.get(`/datasets/${id}/profile/status`);
    return response.data;
  },

  getDatasetStatistics: async (id: string) => {
    const response = await api.get(`/datasets/${id}/statistics`);
    return response.data;
  },

  getColumnStatistics: async (id: string) => {
    const response = await api.get(`/datasets/${id}/columns/statistics`);
    return response.data;
  }
};
