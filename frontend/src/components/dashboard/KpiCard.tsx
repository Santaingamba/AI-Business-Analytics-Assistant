import { TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

interface KpiCardProps {
  title: string;
  value: string | number;
  prefix?: string;
  suffix?: string;
  trend?: number; // percentage change
  trendLabel?: string;
  inverseTrend?: boolean; // if true, positive trend is red, negative is green (e.g. for churn)
  isLoading?: boolean;
}

export function KpiCard({
  title,
  value,
  prefix = '',
  suffix = '',
  trend,
  trendLabel,
  inverseTrend = false,
  isLoading
}: KpiCardProps) {
  
  const isPositive = trend ? trend > 0 : false;
  const isNegative = trend ? trend < 0 : false;
  const isNeutral = trend === 0;

  const getTrendColor = () => {
    if (isNeutral) return 'text-gray-500';
    if (isPositive) return inverseTrend ? 'text-red-600' : 'text-green-600';
    if (isNegative) return inverseTrend ? 'text-green-600' : 'text-red-600';
    return 'text-gray-500';
  };

  const getTrendBg = () => {
    if (isNeutral) return 'bg-gray-100 dark:bg-gray-800';
    if (isPositive) return inverseTrend ? 'bg-red-50 dark:bg-red-900/30' : 'bg-green-50 dark:bg-green-900/30';
    if (isNegative) return inverseTrend ? 'bg-green-50 dark:bg-green-900/30' : 'bg-red-50 dark:bg-red-900/30';
    return 'bg-gray-100 dark:bg-gray-800';
  };

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-100 dark:border-gray-700 transition-all hover:shadow-md relative overflow-hidden">
      {/* Decorative top border */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 opacity-75"></div>
      
      <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400 truncate">{title}</h3>
      
      <div className="mt-2 flex items-baseline gap-2">
        {isLoading ? (
          <div className="h-8 w-24 bg-gray-200 dark:bg-gray-700 animate-pulse rounded"></div>
        ) : (
          <p className="text-3xl font-semibold text-gray-900 dark:text-white tracking-tight">
            {prefix}{typeof value === 'number' ? value.toLocaleString(undefined, { maximumFractionDigits: 2 }) : value}{suffix}
          </p>
        )}
      </div>

      {trend !== undefined && !isLoading && (
        <div className="mt-4 flex items-center text-sm">
          <div className={twMerge(clsx('flex items-center px-2 py-0.5 rounded-full font-medium', getTrendColor(), getTrendBg()))}>
            {isPositive && <TrendingUp className="w-3.5 h-3.5 mr-1" />}
            {isNegative && <TrendingDown className="w-3.5 h-3.5 mr-1" />}
            {isNeutral && <Minus className="w-3.5 h-3.5 mr-1" />}
            {Math.abs(trend)}%
          </div>
          {trendLabel && <span className="ml-2 text-gray-500 dark:text-gray-400 truncate">{trendLabel}</span>}
        </div>
      )}
      
      {isLoading && trend !== undefined && (
        <div className="mt-4 h-5 w-32 bg-gray-200 dark:bg-gray-700 animate-pulse rounded"></div>
      )}
    </div>
  );
}
