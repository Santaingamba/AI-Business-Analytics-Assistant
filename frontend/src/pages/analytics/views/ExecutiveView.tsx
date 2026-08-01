import { useKpis, useMetrics, useChartData } from '../../../hooks/useAnalyticsQuery';
import { KpiCard } from '../../../components/dashboard/KpiCard';
import { WidgetShell } from '../../../components/dashboard/WidgetShell';
import { BaseLineChart } from '../../../components/charts/BaseLineChart';
import { BaseDonutChart } from '../../../components/charts/BaseDonutChart';
import { BaseBarChart } from '../../../components/charts/BaseBarChart';

export function ExecutiveView({ datasetId }: { datasetId: string }) {
  const { data: kpis, isLoading: kpisLoading } = useKpis(datasetId);
  const { data: revMetrics, isLoading: revLoading } = useMetrics(datasetId, 'Revenue');
  const { data: trendMetrics, isLoading: trendLoading } = useMetrics(datasetId, 'Time-Series');

  // Find specific metrics safely
  const dailyRevMetric = trendMetrics?.find(m => m.metric_name === 'Daily Revenue');
  const dailyRevData = useChartData(dailyRevMetric?.value);

  const paymentMethodsMetric = revMetrics?.find(m => m.metric_name === 'Revenue by Payment Method' || m.dimension?.includes('Payment'));
  const paymentData = useChartData(paymentMethodsMetric?.value);

  // If backend doesn't have Payment Method, we can fallback to Sales by Day of Week just to show the chart
  const { data: salesMetrics } = useMetrics(datasetId, 'Sales');
  const dowSalesMetric = salesMetrics?.find(m => m.metric_name === 'Sales by Day of Week');
  const dowData = useChartData(dowSalesMetric?.value);

  return (
    <div className="space-y-6">
      {/* Top KPI Row */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {kpisLoading ? (
          Array.from({ length: 4 }).map((_, i) => <KpiCard key={i} title="Loading..." value={0} isLoading={true} />)
        ) : kpis?.slice(0, 4).map((kpi) => (
          <KpiCard
            key={kpi.id}
            title={kpi.kpi_name}
            value={kpi.value}
            prefix={kpi.kpi_name.includes('Revenue') || kpi.kpi_name.includes('Value') ? '$' : ''}
            suffix={kpi.kpi_name.includes('%') ? '%' : ''}
            trend={0} // Mocked trend until backend provides historical comparison
            trendLabel="vs last period"
          />
        ))}
      </div>

      {/* Main Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <WidgetShell 
            title="Revenue Overview (Time-Series)" 
            isLoading={trendLoading}
            isEmpty={dailyRevData.length === 0}
          >
            <BaseLineChart 
              data={dailyRevData} 
              xAxisKey="name"
              lines={[{ key: 'value', name: 'Revenue', color: '#4f46e5' }]}
              valueFormatter={(val) => `$${val.toLocaleString()}`}
            />
          </WidgetShell>
        </div>
        
        <div className="lg:col-span-1">
          <WidgetShell 
            title={paymentMethodsMetric ? "Revenue by Payment Method" : "Sales by Day of Week"}
            isLoading={revLoading}
            isEmpty={paymentData.length === 0 && dowData.length === 0}
          >
            {paymentData.length > 0 ? (
              <BaseDonutChart 
                data={paymentData}
                nameKey="name"
                dataKey="value"
                valueFormatter={(val) => `$${val.toLocaleString()}`}
              />
            ) : (
              <BaseBarChart 
                data={dowData}
                xAxisKey="name"
                bars={[{ key: 'value', name: 'Sales', color: '#10b981' }]}
                layout="vertical"
                valueFormatter={(val) => `$${val.toLocaleString()}`}
              />
            )}
          </WidgetShell>
        </div>
      </div>
    </div>
  );
}
