import { useMetrics, useChartData } from '../../../hooks/useAnalyticsQuery';
import { WidgetShell } from '../../../components/dashboard/WidgetShell';
import { BaseBarChart } from '../../../components/charts/BaseBarChart';
import { BaseDonutChart } from '../../../components/charts/BaseDonutChart';

export function RevenueView({ datasetId }: { datasetId: string }) {
  const { data: revMetrics, isLoading: revLoading } = useMetrics(datasetId, 'Revenue');

  const catMetric = revMetrics?.find(m => m.metric_name.includes('Category'));
  const catData = useChartData(catMetric?.value);

  const subcatMetric = revMetrics?.find(m => m.metric_name.includes('Sub-Category'));
  const subcatData = useChartData(subcatMetric?.value);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <WidgetShell 
          title="Revenue by Category" 
          isLoading={revLoading}
          isEmpty={catData.length === 0}
        >
          <BaseBarChart 
            data={catData} 
            xAxisKey="name"
            bars={[{ key: 'value', name: 'Revenue', color: '#10b981' }]}
            valueFormatter={(val) => `$${val.toLocaleString()}`}
          />
        </WidgetShell>

        <WidgetShell 
          title="Category Distribution" 
          isLoading={revLoading}
          isEmpty={catData.length === 0}
        >
          <BaseDonutChart 
            data={catData}
            nameKey="name"
            dataKey="value"
            valueFormatter={(val) => `$${val.toLocaleString()}`}
          />
        </WidgetShell>
      </div>

      <WidgetShell 
        title="Revenue by Sub-Category" 
        isLoading={revLoading}
        isEmpty={subcatData.length === 0}
      >
        <BaseBarChart 
          data={subcatData.sort((a: any, b: any) => b.value - a.value).slice(0, 15)} 
          xAxisKey="name"
          bars={[{ key: 'value', name: 'Revenue', color: '#f59e0b' }]}
          layout="vertical"
          height={500}
          valueFormatter={(val) => `$${val.toLocaleString()}`}
        />
      </WidgetShell>
    </div>
  );
}
