import { useState } from 'react';
import { useParams } from 'react-router';
import { useQuery } from '@tanstack/react-query';
import { analyticsService } from '../../services/analytics.service';
import { DashboardProvider } from '../../context/DashboardContext';
import { FilterPanel } from '../../components/dashboard/FilterPanel';
import { ExecutiveView } from './views/ExecutiveView';
import { RevenueView } from './views/RevenueView';
import { CustomerView } from './views/CustomerView';
import { ProductView } from './views/ProductView';
import { Loader2, AlertCircle, TrendingUp, BarChart3, Users, DollarSign, Activity } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

function DashboardShellContent() {
  const { id } = useParams<{ id: string }>();
  const [activeTab, setActiveTab] = useState<'executive' | 'revenue' | 'customers' | 'products' | 'trends'>('executive');
  
  const { data: job, isLoading, isError } = useQuery({
    queryKey: ['analyticsJob', id],
    queryFn: () => analyticsService.getStatus(id!),
    enabled: !!id,
    refetchInterval: (query) => {
        return query.state.data?.status === 'COMPLETED' || query.state.data?.status === 'FAILED' ? false : 3000;
    }
  });

  if (isLoading && !job) {
    return (
      <div className="flex h-[50vh] items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-indigo-600" />
      </div>
    );
  }

  if (isError || job?.status === 'FAILED') {
    return (
      <div className="mx-auto max-w-7xl px-4 py-8">
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <AlertCircle className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <h3 className="text-sm font-medium text-red-800">Dashboard Initialization Failed</h3>
              <p className="mt-2 text-sm text-red-700">{job?.summary?.error || "Analytics could not be processed for this dataset."}</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (job?.status === 'PROCESSING' || job?.status === 'PENDING') {
    return (
      <div className="mx-auto max-w-7xl px-4 py-8 flex flex-col items-center justify-center min-h-[50vh] text-center">
        <Loader2 className="h-10 w-10 animate-spin text-indigo-600 mb-4" />
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white">Processing Analytics</h2>
        <p className="text-gray-500 dark:text-gray-400 max-w-md mt-2">
          The Business Intelligence engine is crunching the numbers. This might take a few moments for large datasets.
        </p>
      </div>
    );
  }

  const tabs = [
    { id: 'executive', name: 'Executive Summary', icon: TrendingUp },
    { id: 'revenue', name: 'Revenue', icon: DollarSign },
    { id: 'customers', name: 'Customers & Segments', icon: Users },
    { id: 'products', name: 'Products & Categories', icon: BarChart3 },
    { id: 'trends', name: 'Trends & Forensics', icon: Activity },
  ] as const;

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 pb-12">
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-5">
          <h1 className="text-2xl font-bold leading-7 text-gray-900 dark:text-white sm:truncate sm:text-3xl sm:tracking-tight">
            Business Intelligence
          </h1>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            Automated analytical insights and metrics.
          </p>
          
          <nav className="-mb-px flex space-x-6 overflow-x-auto mt-6" aria-label="Tabs">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={twMerge(clsx(
                  'group inline-flex items-center border-b-2 py-4 px-1 text-sm font-medium whitespace-nowrap transition-colors',
                  activeTab === tab.id 
                    ? 'border-indigo-500 text-indigo-600 dark:text-indigo-400' 
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300'
                ))}
              >
                <tab.icon className={twMerge(clsx(
                  '-ml-0.5 mr-2 h-5 w-5', 
                  activeTab === tab.id ? 'text-indigo-500 dark:text-indigo-400' : 'text-gray-400 group-hover:text-gray-500 dark:group-hover:text-gray-300'
                ))} />
                {tab.name}
              </button>
            ))}
          </nav>
        </div>
      </div>

      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-8">
        <FilterPanel />
        
        <div className="mt-6">
          {activeTab === 'executive' && <ExecutiveView datasetId={id!} />}
          {activeTab === 'revenue' && <RevenueView datasetId={id!} />}
          {activeTab === 'customers' && <CustomerView datasetId={id!} />}
          {activeTab === 'products' && <ProductView datasetId={id!} />}
          {activeTab === 'trends' && (
            <div className="text-center py-12">
              <Activity className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-semibold text-gray-900 dark:text-white">Trends View</h3>
              <p className="mt-1 text-sm text-gray-500">Currently aggregated into Executive Overview.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function AnalyticsOverview() {
  return (
    <DashboardProvider>
      <DashboardShellContent />
    </DashboardProvider>
  );
}
