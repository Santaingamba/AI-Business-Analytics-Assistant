import { ReactNode } from 'react';
import { Loader2, AlertCircle, Maximize2, Download } from 'lucide-react';

interface WidgetShellProps {
  title: string;
  description?: string;
  isLoading?: boolean;
  error?: string | null;
  isEmpty?: boolean;
  children: ReactNode;
  onExport?: () => void;
  onExpand?: () => void;
}

export function WidgetShell({
  title,
  description,
  isLoading,
  error,
  isEmpty,
  children,
  onExport,
  onExpand,
}: WidgetShellProps) {
  return (
    <div className="flex flex-col rounded-xl bg-white dark:bg-gray-800 shadow-sm border border-gray-100 dark:border-gray-700 h-full overflow-hidden transition-all duration-200 hover:shadow-md">
      <div className="px-5 py-4 border-b border-gray-100 dark:border-gray-700 flex justify-between items-center bg-gray-50/50 dark:bg-gray-800/50">
        <div>
          <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">{title}</h3>
          {description && (
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">{description}</p>
          )}
        </div>
        <div className="flex space-x-2">
          {onExport && (
            <button
              onClick={onExport}
              className="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-md transition-colors"
              title="Export Widget"
            >
              <Download className="w-4 h-4" />
            </button>
          )}
          {onExpand && (
            <button
              onClick={onExpand}
              className="p-1.5 text-gray-400 hover:text-indigo-600 hover:bg-indigo-50 dark:hover:bg-indigo-900/30 rounded-md transition-colors"
              title="Fullscreen"
            >
              <Maximize2 className="w-4 h-4" />
            </button>
          )}
        </div>
      </div>
      <div className="p-5 flex-grow flex flex-col relative min-h-[250px]">
        {isLoading ? (
          <div className="absolute inset-0 z-10 flex items-center justify-center bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
            <Loader2 className="w-8 h-8 animate-spin text-indigo-600" />
          </div>
        ) : error ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6">
            <AlertCircle className="w-8 h-8 text-red-500 mb-2" />
            <p className="text-sm text-red-600 dark:text-red-400 font-medium">Failed to load data</p>
            <p className="text-xs text-gray-500 mt-1">{error}</p>
          </div>
        ) : isEmpty ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center text-center p-6">
            <p className="text-sm text-gray-500 dark:text-gray-400">No data available for the selected filters.</p>
          </div>
        ) : (
          <div className="h-full w-full flex-grow">{children}</div>
        )}
      </div>
    </div>
  );
}
