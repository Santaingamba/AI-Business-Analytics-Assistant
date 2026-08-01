import { useSegments } from '../../../hooks/useAnalyticsQuery';
import { WidgetShell } from '../../../components/dashboard/WidgetShell';
import { BaseBarChart } from '../../../components/charts/BaseBarChart';
import { BaseDonutChart } from '../../../components/charts/BaseDonutChart';
import { Users, DollarSign } from 'lucide-react';

export function CustomerView({ datasetId }: { datasetId: string }) {
  const { data: segments, isLoading: segmentsLoading } = useSegments(datasetId);

  const formattedSegments = segments?.map(s => ({
    name: s.segment_name,
    value: s.customer_count,
    revenue: s.revenue
  })) || [];

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <WidgetShell 
            title="Customer Segments (RFM)" 
            isLoading={segmentsLoading}
            isEmpty={formattedSegments.length === 0}
          >
            <BaseBarChart 
              data={formattedSegments} 
              xAxisKey="name"
              bars={[{ key: 'value', name: 'Customers', color: '#8b5cf6' }]}
            />
          </WidgetShell>
        </div>

        <div className="lg:col-span-1">
          <WidgetShell 
            title="Segment Revenue Contribution" 
            isLoading={segmentsLoading}
            isEmpty={formattedSegments.length === 0}
          >
            <BaseDonutChart 
              data={formattedSegments}
              nameKey="name"
              dataKey="revenue"
              valueFormatter={(val) => `$${val.toLocaleString()}`}
            />
          </WidgetShell>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {segments?.map((seg) => (
          <div key={seg.id} className="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700 p-5">
            <h4 className="font-semibold text-gray-900 dark:text-white">{seg.segment_name}</h4>
            <div className="mt-4 space-y-3">
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-gray-500 dark:text-gray-400">
                  <Users className="w-4 h-4 mr-2" />
                  Count
                </div>
                <span className="font-medium text-gray-900 dark:text-white">{seg.customer_count}</span>
              </div>
              <div className="flex items-center justify-between text-sm">
                <div className="flex items-center text-gray-500 dark:text-gray-400">
                  <DollarSign className="w-4 h-4 mr-2" />
                  Revenue
                </div>
                <span className="font-medium text-gray-900 dark:text-white">
                  ${seg.revenue?.toLocaleString(undefined, { maximumFractionDigits: 0 })}
                </span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
