import { useMetrics, useChartData } from '../../../hooks/useAnalyticsQuery';
import { WidgetShell } from '../../../components/dashboard/WidgetShell';
import { BaseBarChart } from '../../../components/charts/BaseBarChart';

export function ProductView({ datasetId }: { datasetId: string }) {
  const { data: prodMetrics, isLoading } = useMetrics(datasetId, 'Product');

  const topProductsMetric = prodMetrics?.find(m => m.metric_name === 'Top 10 Products by Revenue' || m.dimension?.includes('Product'));
  const topProductsData = useChartData(topProductsMetric?.value);

  const worstProductsMetric = prodMetrics?.find(m => m.metric_name === 'Bottom 10 Products by Revenue');
  const worstProductsData = useChartData(worstProductsMetric?.value);

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <WidgetShell 
          title="Top 10 Products by Revenue" 
          isLoading={isLoading}
          isEmpty={topProductsData.length === 0}
        >
          <BaseBarChart 
            data={topProductsData.sort((a: any, b: any) => b.value - a.value).slice(0, 10)} 
            xAxisKey="name"
            bars={[{ key: 'value', name: 'Revenue', color: '#4f46e5' }]}
            layout="vertical"
            height={400}
            valueFormatter={(val) => `$${val.toLocaleString()}`}
          />
        </WidgetShell>

        <WidgetShell 
          title="Bottom 10 Products by Revenue" 
          isLoading={isLoading}
          isEmpty={worstProductsData.length === 0}
        >
          <BaseBarChart 
            data={worstProductsData.length > 0 ? worstProductsData : topProductsData.sort((a: any, b: any) => a.value - b.value).slice(0, 10)} 
            xAxisKey="name"
            bars={[{ key: 'value', name: 'Revenue', color: '#ef4444' }]}
            layout="vertical"
            height={400}
            valueFormatter={(val) => `$${val.toLocaleString()}`}
          />
        </WidgetShell>
      </div>
    </div>
  );
}
