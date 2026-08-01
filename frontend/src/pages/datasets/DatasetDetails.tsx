import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router';
import { 
  Database, ArrowLeft, Trash2, Calendar, FileText, TableProperties, 
  Settings, AlertCircle, Hash, Type, AlignLeft, ShieldCheck, Activity, BarChart3
} from 'lucide-react';
import { datasetService } from '../../services/dataset.service';
import { DatasetDetails as IDatasetDetails, DatasetPreview, DatasetColumn } from '../../types/dataset';
import { format } from 'date-fns';
import { Link } from 'react-router';

export const DatasetDetails: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [dataset, setDataset] = useState<IDatasetDetails | null>(null);
  const [preview, setPreview] = useState<DatasetPreview | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'overview' | 'schema' | 'preview'>('overview');

  useEffect(() => {
    const fetchData = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const [datasetData, previewData] = await Promise.all([
          datasetService.getDatasetDetails(id),
          datasetService.getDatasetPreview(id).catch(() => null)
        ]);
        
        setDataset((datasetData as any).data || datasetData);
        if (previewData) {
          setPreview((previewData as any).data || previewData);
        }
      } catch (err: any) {
        setError(err.response?.data?.message || 'Failed to load dataset details');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id]);

  const handleDelete = async () => {
    if (!id || !confirm('Are you sure you want to delete this dataset? This action cannot be undone.')) return;
    try {
      await datasetService.deleteDataset(id);
      navigate('/datasets');
    } catch (err: any) {
      alert('Failed to delete dataset: ' + (err.response?.data?.message || err.message));
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[50vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
      </div>
    );
  }

  if (error || !dataset) {
    return (
      <div className="max-w-7xl mx-auto px-4 py-12 text-center">
        <AlertCircle className="mx-auto h-12 w-12 text-red-500 mb-4" />
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">Error Loading Dataset</h2>
        <p className="text-gray-500 dark:text-gray-400 mb-6">{error || 'Dataset not found'}</p>
        <button onClick={() => navigate('/datasets')} className="text-primary-600 font-medium hover:underline">
          &larr; Back to Catalog
        </button>
      </div>
    );
  }

  const getDataTypeIcon = (type: string) => {
    switch (type) {
      case 'INTEGER':
      case 'FLOAT': return <Hash className="h-4 w-4 text-blue-500" />;
      case 'STRING': return <Type className="h-4 w-4 text-green-500" />;
      case 'BOOLEAN': return <ShieldCheck className="h-4 w-4 text-purple-500" />;
      default: return <AlignLeft className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 animate-fade-in-up">
      {/* Header */}
      <div className="mb-6">
        <Link to="/datasets" className="inline-flex items-center text-sm font-medium text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 mb-4 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back to Catalog
        </Link>
        <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-primary-50 dark:bg-primary-900/20 rounded-xl">
              <Database className="h-8 w-8 text-primary-600 dark:text-primary-400" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center gap-2">
                {dataset.display_name}
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  dataset.processing_status === 'READY' ? 'bg-green-100 text-green-800' : 
                  dataset.processing_status === 'FAILED' ? 'bg-red-100 text-red-800' : 
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {dataset.processing_status}
                </span>
              </h1>
              <p className="mt-1 flex items-center text-sm text-gray-500 dark:text-gray-400 font-mono">
                {dataset.original_filename} • {(dataset.file_size_bytes / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <Link 
            to={`/datasets/${id}/profile`}
            className="inline-flex items-center px-4 py-2 border border-primary-300 dark:border-primary-800 shadow-sm text-sm font-medium rounded-md text-primary-700 dark:text-primary-400 bg-primary-50 dark:bg-primary-900/20 hover:bg-primary-100 dark:hover:bg-primary-900/40 transition-colors focus:outline-none"
          >
            <Activity className="-ml-1 mr-2 h-4 w-4" />
            Data Intelligence
          </Link>
          <Link 
            to={`/datasets/${id}/analytics`}
            className="inline-flex items-center px-4 py-2 border border-indigo-300 dark:border-indigo-800 shadow-sm text-sm font-medium rounded-md text-indigo-700 dark:text-indigo-400 bg-indigo-50 dark:bg-indigo-900/20 hover:bg-indigo-100 dark:hover:bg-indigo-900/40 transition-colors focus:outline-none"
          >
            <BarChart3 className="-ml-1 mr-2 h-4 w-4" />
            Business Intelligence
          </Link>
          <button 
            onClick={handleDelete}
            className="inline-flex items-center px-4 py-2 border border-red-300 dark:border-red-800 shadow-sm text-sm font-medium rounded-md text-red-700 dark:text-red-400 bg-white dark:bg-gray-800 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors focus:outline-none"
          >
            <Trash2 className="-ml-1 mr-2 h-4 w-4" />
            Delete Dataset
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700 mb-8">
        <nav className="-mb-px flex space-x-8">
          {[
            { id: 'overview', name: 'Overview', icon: FileText },
            { id: 'schema', name: 'Schema', icon: Settings },
            { id: 'preview', name: 'Data Preview', icon: TableProperties },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`
                whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm flex items-center transition-colors
                ${activeTab === tab.id 
                  ? 'border-primary-500 text-primary-600 dark:text-primary-400' 
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-gray-300 dark:hover:border-gray-600'
                }
              `}
            >
              <tab.icon className={`mr-2 h-4 w-4 ${activeTab === tab.id ? 'text-primary-500' : 'text-gray-400'}`} />
              {tab.name}
            </button>
          ))}
        </nav>
      </div>

      {/* Tab Content */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-6 min-h-[400px]">
        {activeTab === 'overview' && (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="md:col-span-2 space-y-6">
              <div>
                <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">Description</h3>
                <p className="text-gray-600 dark:text-gray-300">
                  {dataset.description || 'No description provided for this dataset.'}
                </p>
              </div>
              
              <div className="grid grid-cols-2 gap-4">
                <div className="bg-gray-50 dark:bg-gray-750 p-4 rounded-lg border border-gray-100 dark:border-gray-700">
                  <span className="block text-sm text-gray-500 dark:text-gray-400 mb-1">Total Rows</span>
                  <span className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {dataset.row_count ? dataset.row_count.toLocaleString() : '-'}
                  </span>
                </div>
                <div className="bg-gray-50 dark:bg-gray-750 p-4 rounded-lg border border-gray-100 dark:border-gray-700">
                  <span className="block text-sm text-gray-500 dark:text-gray-400 mb-1">Total Columns</span>
                  <span className="text-2xl font-semibold text-gray-900 dark:text-white">
                    {dataset.column_count ? dataset.column_count.toLocaleString() : '-'}
                  </span>
                </div>
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-4">Metadata</h3>
              <ul className="space-y-4">
                <li className="flex justify-between items-center text-sm border-b border-gray-100 dark:border-gray-700 pb-2">
                  <span className="text-gray-500 flex items-center gap-2">
                    <Calendar className="h-4 w-4" /> Uploaded Date
                  </span>
                  <span className="font-medium text-gray-900 dark:text-white">
                    {format(new Date(dataset.created_at), 'MMM d, yyyy')}
                  </span>
                </li>
                <li className="flex justify-between items-center text-sm border-b border-gray-100 dark:border-gray-700 pb-2">
                  <span className="text-gray-500 flex items-center gap-2">
                    <FileText className="h-4 w-4" /> Format
                  </span>
                  <span className="font-medium text-gray-900 dark:text-white">{dataset.file_type}</span>
                </li>
                <li className="flex justify-between items-center text-sm border-b border-gray-100 dark:border-gray-700 pb-2">
                  <span className="text-gray-500 flex items-center gap-2">
                    <ShieldCheck className="h-4 w-4" /> Visibility
                  </span>
                  <span className="font-medium text-gray-900 dark:text-white capitalize">{dataset.visibility.toLowerCase()}</span>
                </li>
              </ul>
            </div>
          </div>
        )}

        {activeTab === 'schema' && (
          <div>
            <div className="overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
              <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-750/50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Column Name</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Data Type</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Nullable</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Null Count</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Sample Values</th>
                  </tr>
                </thead>
                <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                  {dataset.columns?.length > 0 ? (
                    dataset.columns.map((col: DatasetColumn) => (
                      <tr key={col.id} className="hover:bg-gray-50 dark:hover:bg-gray-750/50 transition-colors">
                        <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                          {col.column_name}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          <span className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200">
                            {getDataTypeIcon(col.data_type)}
                            {col.data_type}
                          </span>
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {col.is_nullable ? 'Yes' : 'No'}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                          {col.null_count !== null ? col.null_count.toLocaleString() : 'N/A'}
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-500 truncate max-w-xs">
                          {col.sample_values ? col.sample_values.join(', ') : 'N/A'}
                        </td>
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={5} className="px-6 py-12 text-center text-sm text-gray-500">
                        Schema extraction is still processing or failed.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'preview' && (
          <div>
            {!preview ? (
              <div className="py-12 text-center text-gray-500">
                Preview not available yet.
              </div>
            ) : (
              <div className="overflow-x-auto border border-gray-200 dark:border-gray-700 rounded-lg">
                <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
                  <thead className="bg-gray-50 dark:bg-gray-750/50">
                    <tr>
                      {preview.headers.map((header, idx) => (
                        <th key={idx} className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider whitespace-nowrap">
                          {header}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
                    {preview.data.map((row, rowIdx) => (
                      <tr key={rowIdx} className="hover:bg-gray-50 dark:hover:bg-gray-750/50 transition-colors">
                        {row.map((cell, cellIdx) => (
                          <td key={cellIdx} className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 truncate max-w-[200px]" title={String(cell)}>
                            {String(cell)}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            <div className="mt-4 text-sm text-gray-500 text-right">
              Showing top {preview?.data?.length || 0} rows
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
