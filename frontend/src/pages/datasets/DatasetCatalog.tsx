import React, { useEffect, useState } from 'react';
import { Link } from 'react-router';
import { Database, Plus, Search, FileText, TableProperties, Clock, Trash2 } from 'lucide-react';
import { datasetService } from '../../services/dataset.service';
import { Dataset } from '../../types/dataset';
import { formatDistanceToNow } from 'date-fns';

export const DatasetCatalog: React.FC = () => {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  const fetchDatasets = async () => {
    try {
      setLoading(true);
      const data = await datasetService.getDatasets(0, 100, search);
      setDatasets(data);
    } catch (error) {
      console.error('Failed to fetch datasets:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDatasets();
  }, [search]);

  const handleDelete = async (e: React.MouseEvent, id: string) => {
    e.preventDefault();
    if (!confirm('Are you sure you want to delete this dataset?')) return;
    try {
      await datasetService.deleteDataset(id);
      setDatasets(datasets.filter(d => d.id !== id));
    } catch (error) {
      console.error('Failed to delete dataset:', error);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-fade-in-up">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
            <Database className="h-8 w-8 text-primary-500" />
            Data Catalog
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Manage, explore, and analyze your datasets securely.
          </p>
        </div>
        <Link
          to="/datasets/upload"
          className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 transition-colors"
        >
          <Plus className="-ml-1 mr-2 h-5 w-5" />
          Upload Dataset
        </Link>
      </div>

      <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
        <div className="relative rounded-md shadow-sm max-w-md">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
          <input
            type="text"
            className="focus:ring-primary-500 focus:border-primary-500 block w-full pl-10 sm:text-sm border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-md transition-colors"
            placeholder="Search datasets..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </div>

      {loading ? (
        <div className="flex justify-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500"></div>
        </div>
      ) : datasets.length === 0 ? (
        <div className="text-center py-16 bg-white dark:bg-gray-800 rounded-xl border border-dashed border-gray-300 dark:border-gray-700">
          <Database className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900 dark:text-white">No datasets</h3>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Get started by creating a new dataset.
          </p>
          <div className="mt-6">
            <Link
              to="/datasets/upload"
              className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-primary-700 bg-primary-100 hover:bg-primary-200 transition-colors"
            >
              <Plus className="-ml-1 mr-2 h-5 w-5" />
              New Dataset
            </Link>
          </div>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {datasets.map((dataset) => (
            <Link
              key={dataset.id}
              to={`/datasets/${dataset.id}`}
              className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 hover:shadow-md hover:border-primary-300 transition-all group overflow-hidden flex flex-col"
            >
              <div className="p-5 flex-grow">
                <div className="flex justify-between items-start">
                  <div className="flex items-center gap-3">
                    <div className="p-2 bg-primary-50 dark:bg-primary-900/20 rounded-lg">
                      <FileText className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                    </div>
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 dark:text-white group-hover:text-primary-600 transition-colors line-clamp-1">
                        {dataset.display_name}
                      </h3>
                      <p className="text-xs text-gray-500 dark:text-gray-400 font-mono">
                        {dataset.file_type} • {(dataset.file_size_bytes / 1024 / 1024).toFixed(2)} MB
                      </p>
                    </div>
                  </div>
                  <button 
                    onClick={(e) => handleDelete(e, dataset.id)}
                    className="text-gray-400 hover:text-red-500 transition-colors p-1"
                  >
                    <Trash2 className="h-5 w-5" />
                  </button>
                </div>
                
                <p className="mt-4 text-sm text-gray-600 dark:text-gray-300 line-clamp-2 min-h-[2.5rem]">
                  {dataset.description || 'No description provided.'}
                </p>

                <div className="mt-5 grid grid-cols-2 gap-4 text-sm text-gray-500 dark:text-gray-400">
                  <div className="flex items-center gap-2">
                    <TableProperties className="h-4 w-4" />
                    <span>{dataset.row_count ? dataset.row_count.toLocaleString() : '-'} rows</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Clock className="h-4 w-4" />
                    <span>{formatDistanceToNow(new Date(dataset.created_at))} ago</span>
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-750 px-5 py-3 border-t border-gray-100 dark:border-gray-700 flex justify-between items-center">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  dataset.processing_status === 'READY' ? 'bg-green-100 text-green-800' : 
                  dataset.processing_status === 'FAILED' ? 'bg-red-100 text-red-800' : 
                  'bg-yellow-100 text-yellow-800'
                }`}>
                  {dataset.processing_status}
                </span>
                <span className="text-xs text-gray-500">{dataset.visibility.toLowerCase()}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
