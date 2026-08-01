import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router';
import { 
  Activity, Database, AlertTriangle, 
  RefreshCw, Server, AlertCircle, Loader
} from 'lucide-react';
import { datasetService } from '../../services/dataset.service';
import { DatasetStatistics, ColumnStatistics, ProcessingJob } from '../../types/dataset';

export const DatasetProfile: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [stats, setStats] = useState<DatasetStatistics | null>(null);
  const [colStats, setColStats] = useState<ColumnStatistics[]>([]);
  const [job, setJob] = useState<ProcessingJob | null>(null);
  const [loading, setLoading] = useState(true);
  const [triggering, setTriggering] = useState(false);

  const fetchProfile = async () => {
    if (!id) return;
    try {
      setLoading(true);
      const statusRes = await datasetService.getProfilingStatus(id).catch(() => null);
      setJob((statusRes as any)?.data || statusRes);
      
      const statsRes = await datasetService.getDatasetStatistics(id).catch(() => null);
      if (statsRes) {
        setStats((statsRes as any).data || statsRes);
      }
      
      const colsRes = await datasetService.getColumnStatistics(id).catch(() => null);
      if (colsRes) {
        setColStats((colsRes as any).data || colsRes);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchProfile();
    
    const interval = setInterval(() => {
      if (job?.status === 'RUNNING' || job?.status === 'PENDING') {
        fetchProfile();
      }
    }, 3000);
    
    return () => clearInterval(interval);
  }, [id, job?.status]);

  const handleTrigger = async () => {
    if (!id) return;
    try {
      setTriggering(true);
      await datasetService.triggerProfiling(id);
      fetchProfile();
    } catch (err) {
      alert('Failed to trigger profiling');
    } finally {
      setTriggering(false);
    }
  };

  const getScoreColor = (score: number | null) => {
    if (score === null) return 'text-gray-500';
    if (score >= 90) return 'text-green-500';
    if (score >= 70) return 'text-yellow-500';
    return 'text-red-500';
  };

  if (loading && !stats) {
    return (
      <div className="flex justify-center py-20">
        <Loader className="h-8 w-8 animate-spin text-primary-500" />
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-fade-in-up">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <Activity className="h-8 w-8 text-primary-500" />
            Data Intelligence Profile
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Comprehensive statistical analysis and quality assessment
          </p>
        </div>
        <div>
          <button 
            onClick={handleTrigger}
            disabled={triggering || job?.status === 'RUNNING'}
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700 disabled:opacity-50 transition-colors shadow-sm font-medium"
          >
            {job?.status === 'RUNNING' || job?.status === 'PENDING' ? (
              <><Loader className="animate-spin -ml-1 mr-2 h-5 w-5" /> Profiling...</>
            ) : (
              <><RefreshCw className="-ml-1 mr-2 h-5 w-5" /> Run Full Profile</>
            )}
          </button>
        </div>
      </div>

      {job && job.status === 'FAILED' && (
        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-md flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-500 mt-0.5" />
          <div>
            <h4 className="text-sm font-medium text-red-800">Profiling Failed</h4>
            <p className="text-sm text-red-700 mt-1">{job.summary?.error || 'Unknown error occurred during processing.'}</p>
          </div>
        </div>
      )}

      {stats ? (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Quality Score</div>
              <div className={`text-4xl font-bold ${getScoreColor(stats.quality_score)}`}>
                {stats.quality_score !== null ? `${stats.quality_score.toFixed(1)}` : 'N/A'}
                <span className="text-lg font-normal text-gray-400 ml-1">/ 100</span>
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Completeness</div>
              <div className={`text-4xl font-bold ${getScoreColor(stats.completeness_score)}`}>
                {stats.completeness_score !== null ? `${stats.completeness_score.toFixed(1)}%` : 'N/A'}
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Total Dimensions</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white">
                {stats.row_count.toLocaleString()} <span className="text-sm font-normal text-gray-500">rows</span>
              </div>
              <div className="text-sm text-gray-500">
                × {stats.column_count.toLocaleString()} columns
              </div>
            </div>
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-1">Memory Usage</div>
              <div className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                <Server className="h-5 w-5 text-blue-500" />
                {stats.memory_usage_bytes ? (stats.memory_usage_bytes / 1024 / 1024).toFixed(2) : 0} MB
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Column Distribution</h3>
              <div className="space-y-5">
                {[
                  { label: 'Numeric', count: stats.numeric_columns, color: 'bg-blue-500' },
                  { label: 'Categorical/Text', count: stats.text_columns, color: 'bg-purple-500' },
                  { label: 'Boolean', count: stats.boolean_columns, color: 'bg-green-500' },
                  { label: 'DateTime', count: stats.datetime_columns, color: 'bg-yellow-500' }
                ].map(type => (
                  <div key={type.label}>
                    <div className="flex justify-between text-sm mb-1.5">
                      <span className="text-gray-600 dark:text-gray-300 font-medium">{type.label}</span>
                      <span className="font-semibold text-gray-900 dark:text-white">{type.count}</span>
                    </div>
                    <div className="w-full bg-gray-100 dark:bg-gray-700 rounded-full h-2">
                      <div 
                        className={`${type.color} h-2 rounded-full transition-all duration-1000`} 
                        style={{ width: `${stats.column_count > 0 ? (type.count / stats.column_count) * 100 : 0}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="bg-white dark:bg-gray-800 p-6 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Data Health Anomalies</h3>
              <ul className="space-y-4">
                <li className="flex items-start gap-4 p-4 rounded-xl bg-red-50 dark:bg-red-900/10 border border-red-100 dark:border-red-900/30">
                  <div className="p-2 bg-red-100 dark:bg-red-900/30 rounded-lg">
                    <AlertTriangle className="h-6 w-6 text-red-600 dark:text-red-500" />
                  </div>
                  <div>
                    <h4 className="text-base font-semibold text-red-800 dark:text-red-400">Missing Values</h4>
                    <p className="text-sm text-red-600 dark:text-red-500 mt-1">
                      {stats.null_cells.toLocaleString()} cells ({stats.row_count * stats.column_count > 0 ? ((stats.null_cells / (stats.row_count * stats.column_count)) * 100).toFixed(2) : 0}%) are missing across the dataset.
                    </p>
                  </div>
                </li>
                <li className="flex items-start gap-4 p-4 rounded-xl bg-yellow-50 dark:bg-yellow-900/10 border border-yellow-100 dark:border-yellow-900/30">
                  <div className="p-2 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg">
                    <Database className="h-6 w-6 text-yellow-600 dark:text-yellow-500" />
                  </div>
                  <div>
                    <h4 className="text-base font-semibold text-yellow-800 dark:text-yellow-400">Exact Duplicates</h4>
                    <p className="text-sm text-yellow-600 dark:text-yellow-500 mt-1">
                      {stats.duplicate_rows.toLocaleString()} exact duplicate rows found in the set.
                    </p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
          
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
            <div className="px-6 py-5 border-b border-gray-100 dark:border-gray-700 bg-gray-50 dark:bg-gray-750/50">
              <h3 className="text-lg font-medium text-gray-900 dark:text-white">Detailed Column Analytics</h3>
            </div>
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700 text-sm">
                <thead className="bg-gray-50/50 dark:bg-gray-800">
                  <tr>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Column (UUID)</th>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Semantic Type</th>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Missing</th>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Outliers</th>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Mean</th>
                    <th className="px-6 py-4 text-left font-semibold text-gray-600 dark:text-gray-300">Std Dev</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100 dark:divide-gray-700">
                  {colStats.map(c => (
                    <tr key={c.id} className="hover:bg-gray-50/80 dark:hover:bg-gray-750/50 transition-colors">
                      <td className="px-6 py-4 font-mono text-xs text-gray-500 dark:text-gray-400 truncate max-w-[150px]" title={c.column_id}>{c.column_id}</td>
                      <td className="px-6 py-4">
                        <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400 border border-blue-100 dark:border-blue-800">
                          {c.semantic_type || 'Unknown'}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <span className={c.missing_percentage > 10 ? 'text-red-500 font-semibold' : 'text-gray-600 dark:text-gray-300'}>
                          {c.missing_percentage.toFixed(1)}%
                        </span>
                      </td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-300">
                        {c.outlier_count > 0 ? (
                          <span className="inline-flex items-center gap-1 text-yellow-600 dark:text-yellow-500">
                            <AlertTriangle className="h-3 w-3" /> {c.outlier_count}
                          </span>
                        ) : '-'}
                      </td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-300">{c.mean !== null ? c.mean.toFixed(2) : '-'}</td>
                      <td className="px-6 py-4 text-gray-600 dark:text-gray-300">{c.std_dev !== null ? c.std_dev.toFixed(2) : '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

        </div>
      ) : (
        <div className="text-center py-20 bg-white dark:bg-gray-800 rounded-xl border border-dashed border-gray-300 dark:border-gray-700">
          <Activity className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">No Intelligence Profile Available</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Run a full statistical profile to generate intelligence metrics.
          </p>
          <div className="mt-6">
            <button
              onClick={handleTrigger}
              className="inline-flex items-center px-6 py-2.5 shadow-sm text-sm font-medium rounded-lg text-white bg-primary-600 hover:bg-primary-700 transition-colors"
            >
              <RefreshCw className="-ml-1 mr-2 h-5 w-5" />
              Start Profiling
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
