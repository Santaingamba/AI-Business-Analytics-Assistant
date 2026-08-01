import React, { useState, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router';
import { UploadCloud, File, X, CheckCircle, AlertCircle, Database } from 'lucide-react';
import { datasetService } from '../../services/dataset.service';

export const DatasetUpload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [displayName, setDisplayName] = useState('');
  const [description, setDescription] = useState('');
  const [isDragging, setIsDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const navigate = useNavigate();

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && validateFile(droppedFile)) {
      setFile(droppedFile);
      if (!displayName) setDisplayName(droppedFile.name);
    }
  }, [displayName]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files?.[0];
    if (selectedFile && validateFile(selectedFile)) {
      setFile(selectedFile);
      if (!displayName) setDisplayName(selectedFile.name);
    }
  };

  const validateFile = (file: File) => {
    const validTypes = ['text/csv', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'];
    if (!validTypes.includes(file.type) && !file.name.endsWith('.csv') && !file.name.endsWith('.xlsx')) {
      setError('Please upload a valid CSV or Excel file.');
      return false;
    }
    if (file.size > 500 * 1024 * 1024) { // 500MB
      setError('File size must be less than 500MB.');
      return false;
    }
    setError(null);
    return true;
  };

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    try {
      setUploading(true);
      setError(null);
      const dataset = await datasetService.uploadDataset(
        file,
        displayName || file.name,
        description,
        (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setProgress(percentCompleted);
          }
        }
      );
      
      const id = (dataset as any)?.data?.id || dataset.id;
      navigate(`/datasets/${id}`);
    } catch (err: any) {
      setError(err.response?.data?.message || err.message || 'Failed to upload dataset');
      setProgress(0);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in-up">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center gap-3">
          <Database className="h-8 w-8 text-primary-500" />
          Upload Dataset
        </h1>
        <p className="mt-2 text-sm text-gray-500 dark:text-gray-400">
          Upload your data files to start exploring and analyzing them. We support CSV and Excel files up to 500MB.
        </p>
      </div>

      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-sm border border-gray-100 dark:border-gray-700 overflow-hidden">
        <div className="p-6 sm:p-8">
          <form onSubmit={handleUpload} className="space-y-6">
            
            <div 
              className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
                isDragging ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' : 
                file ? 'border-green-300 bg-green-50 dark:bg-green-900/10' : 
                'border-gray-300 dark:border-gray-600 hover:border-primary-400 dark:hover:border-primary-500'
              }`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => !file && fileInputRef.current?.click()}
            >
              <input 
                type="file" 
                ref={fileInputRef} 
                onChange={handleFileChange} 
                className="hidden" 
                accept=".csv,.xlsx,.xls" 
              />
              
              {!file ? (
                <div className="flex flex-col items-center cursor-pointer">
                  <div className="p-4 bg-primary-50 dark:bg-primary-900/20 rounded-full mb-4">
                    <UploadCloud className="h-10 w-10 text-primary-500" />
                  </div>
                  <p className="text-base font-medium text-gray-900 dark:text-white">
                    Click to upload or drag and drop
                  </p>
                  <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
                    CSV or Excel (max. 500MB)
                  </p>
                </div>
              ) : (
                <div className="flex items-center justify-between bg-white dark:bg-gray-750 p-4 rounded-lg border border-gray-200 dark:border-gray-600 shadow-sm cursor-default">
                  <div className="flex items-center gap-4">
                    <div className="p-2 bg-green-100 dark:bg-green-900/30 rounded-lg">
                      <File className="h-8 w-8 text-green-600 dark:text-green-400" />
                    </div>
                    <div className="text-left">
                      <p className="text-sm font-medium text-gray-900 dark:text-white line-clamp-1">{file.name}</p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                    </div>
                  </div>
                  <button 
                    type="button" 
                    onClick={(e) => { e.stopPropagation(); setFile(null); }}
                    className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                  >
                    <X className="h-5 w-5" />
                  </button>
                </div>
              )}
            </div>

            {error && (
              <div className="p-4 rounded-md bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 flex items-start gap-3">
                <AlertCircle className="h-5 w-5 text-red-600 dark:text-red-400 mt-0.5" />
                <p className="text-sm text-red-800 dark:text-red-300">{error}</p>
              </div>
            )}

            {file && (
              <div className="space-y-4 animate-fade-in">
                <div>
                  <label htmlFor="displayName" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Dataset Name
                  </label>
                  <input
                    type="text"
                    id="displayName"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    className="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                    placeholder="E.g., Q3 Sales Data"
                    required
                  />
                </div>
                <div>
                  <label htmlFor="description" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Description (Optional)
                  </label>
                  <textarea
                    id="description"
                    rows={3}
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    className="block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-primary-500 focus:ring-primary-500 sm:text-sm dark:bg-gray-700 dark:text-white"
                    placeholder="Add some context about this dataset..."
                  />
                </div>
              </div>
            )}

            <div className="pt-4 flex justify-end gap-3 border-t border-gray-100 dark:border-gray-700">
              <button
                type="button"
                onClick={() => navigate('/datasets')}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 hover:bg-gray-50 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={!file || uploading}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {uploading ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                    Uploading... {progress}%
                  </>
                ) : (
                  <>
                    <CheckCircle className="-ml-1 mr-2 h-4 w-4" />
                    Upload Dataset
                  </>
                )}
              </button>
            </div>
            
            {uploading && (
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-1.5 mt-4 overflow-hidden">
                <div 
                  className="bg-primary-600 h-1.5 rounded-full transition-all duration-300" 
                  style={{ width: `${progress}%` }}
                ></div>
              </div>
            )}
          </form>
        </div>
      </div>
    </div>
  );
};
