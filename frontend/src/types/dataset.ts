export type FileType = 'CSV' | 'EXCEL';
export type ProcessingStatus = 'UPLOADING' | 'PROCESSING' | 'READY' | 'FAILED';
export type Visibility = 'PRIVATE' | 'ORG' | 'PUBLIC';
export type ColumnDataType = 'STRING' | 'INTEGER' | 'FLOAT' | 'BOOLEAN' | 'DATETIME' | 'UNKNOWN';

export interface Dataset {
  id: string;
  owner_id: string;
  original_filename: string;
  stored_filename: string;
  display_name: string;
  description: string | null;
  file_type: FileType;
  file_size_bytes: number;
  processing_status: ProcessingStatus;
  visibility: Visibility;
  row_count: number | null;
  column_count: number | null;
  created_at: string;
  updated_at: string;
}

export interface DatasetColumn {
  id: string;
  dataset_id: string;
  column_name: string;
  data_type: ColumnDataType;
  sample_values: string[] | null;
  null_count: number | null;
  is_nullable: boolean;
}

export interface DatasetDetails extends Dataset {
  columns: DatasetColumn[];
}

export interface DatasetPreview {
  headers: string[];
  data: any[][];
  row_count: number;
  column_count: number;
}

export interface DatasetStatistics {
  id: string;
  dataset_id: string;
  row_count: number;
  column_count: number;
  numeric_columns: number;
  categorical_columns: number;
  boolean_columns: number;
  datetime_columns: number;
  text_columns: number;
  memory_usage_bytes: number | null;
  null_cells: number;
  duplicate_rows: number;
  duplicate_columns: number;
  completeness_score: number | null;
  quality_score: number | null;
}

export interface ColumnStatistics {
  id: string;
  dataset_id: string;
  column_id: string;
  mean: number | null;
  median: number | null;
  mode: string | null;
  variance: number | null;
  std_dev: number | null;
  min_val: number | null;
  max_val: number | null;
  range_val: number | null;
  q1: number | null;
  q3: number | null;
  iqr: number | null;
  missing_count: number;
  missing_percentage: number;
  unique_count: number;
  unique_percentage: number;
  duplicate_percentage: number;
  outlier_count: number;
  outlier_percentage: number;
  skewness: number | null;
  kurtosis: number | null;
  entropy: number | null;
  semantic_type: string | null;
}

export interface ProcessingJob {
  id: string;
  dataset_id: string;
  status: 'PENDING' | 'RUNNING' | 'COMPLETED' | 'FAILED';
  processing_version: string;
  started_at: string | null;
  completed_at: string | null;
  duration_ms: number | null;
  summary: any | null;
}
