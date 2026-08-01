import React from 'react';
import { useDashboard } from '../../context/DashboardContext';
import { Filter, X } from 'lucide-react';

export function FilterPanel() {
  const { filters, setFilters, resetFilters } = useDashboard();

  const handleCategoryChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setFilters({ category: val === 'all' ? null : val });
  };

  const handleSegmentChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const val = e.target.value;
    setFilters({ customerSegment: val === 'all' ? null : val });
  };

  const hasActiveFilters = filters.category || filters.customerSegment || filters.region || filters.dateRange[0];

  return (
    <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg border border-gray-200 dark:border-gray-700 p-4 mb-6 transition-colors">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center text-sm font-medium text-gray-700 dark:text-gray-300">
          <Filter className="w-4 h-4 mr-2 text-gray-400" />
          Global Filters
        </div>
        
        <div className="flex flex-wrap items-center gap-3">
          <select
            value={filters.category || 'all'}
            onChange={handleCategoryChange}
            className="block w-full sm:w-auto rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:text-white dark:ring-gray-600"
          >
            <option value="all">All Categories</option>
            {/* These would normally be populated dynamically from backend metadata */}
            <option value="Electronics">Electronics</option>
            <option value="Clothing">Clothing</option>
            <option value="Home">Home</option>
          </select>

          <select
            value={filters.customerSegment || 'all'}
            onChange={handleSegmentChange}
            className="block w-full sm:w-auto rounded-md border-0 py-1.5 pl-3 pr-10 text-gray-900 ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6 dark:bg-gray-700 dark:text-white dark:ring-gray-600"
          >
            <option value="all">All Segments</option>
            <option value="Champions">Champions</option>
            <option value="Loyal">Loyal</option>
            <option value="At Risk">At Risk</option>
            <option value="Recent">Recent</option>
          </select>

          {hasActiveFilters && (
            <button
              onClick={resetFilters}
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
            >
              <X className="w-4 h-4 mr-1" />
              Reset
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
