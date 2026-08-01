import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';

interface BaseBarChartProps {
  data: any[];
  xAxisKey: string;
  bars: {
    key: string;
    name: string;
    color?: string;
    stacked?: boolean;
  }[];
  height?: number;
  valueFormatter?: (value: number) => string;
  layout?: 'horizontal' | 'vertical';
}

const DEFAULT_COLORS = ['#4f46e5', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];

export function BaseBarChart({
  data,
  xAxisKey,
  bars,
  height = 300,
  valueFormatter,
  layout = 'horizontal'
}: BaseBarChartProps) {
  const isVertical = layout === 'vertical';

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <BarChart 
          data={data} 
          layout={layout}
          margin={{ top: 5, right: 30, left: isVertical ? 50 : 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" horizontal={!isVertical} vertical={isVertical} stroke="#e5e7eb" />
          
          <XAxis 
            dataKey={isVertical ? undefined : xAxisKey} 
            type={isVertical ? 'number' : 'category'}
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6b7280', fontSize: 12 }} 
            dy={10}
            tickFormatter={isVertical ? valueFormatter : undefined}
          />
          <YAxis 
            dataKey={isVertical ? xAxisKey : undefined}
            type={isVertical ? 'category' : 'number'}
            axisLine={false} 
            tickLine={false} 
            tick={{ fill: '#6b7280', fontSize: 12 }}
            tickFormatter={!isVertical ? valueFormatter : undefined}
            dx={-10}
          />
          
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            formatter={(value: any, name: any) => [valueFormatter ? valueFormatter(value) : value, name]}
            cursor={{ fill: '#f3f4f6' }}
          />
          <Legend wrapperStyle={{ paddingTop: '20px' }} iconType="circle" />
          
          {bars.map((bar, index) => (
            <Bar
              key={bar.key}
              dataKey={bar.key}
              name={bar.name}
              fill={bar.color || DEFAULT_COLORS[index % DEFAULT_COLORS.length]}
              stackId={bar.stacked ? 'stack' : undefined}
              radius={isVertical ? [0, 4, 4, 0] : [4, 4, 0, 0]}
              maxBarSize={50}
            />
          ))}
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
