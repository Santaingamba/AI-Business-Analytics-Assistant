import { useState } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  Legend
} from 'recharts';

interface BaseDonutChartProps {
  data: any[];
  nameKey: string;
  dataKey: string;
  height?: number;
  valueFormatter?: (value: number) => string;
  colors?: string[];
}

const DEFAULT_COLORS = ['#4f46e5', '#818cf8', '#c7d2fe', '#3730a3', '#1e1b4b', '#10b981', '#34d399'];

export function BaseDonutChart({
  data,
  nameKey,
  dataKey,
  height = 300,
  valueFormatter,
  colors = DEFAULT_COLORS
}: BaseDonutChartProps) {
  const [activeIndex, setActiveIndex] = useState(-1);

  const onPieEnter = (_: any, index: number) => {
    setActiveIndex(index);
  };
  
  const onPieLeave = () => {
    setActiveIndex(-1);
  };

  return (
    <div style={{ width: '100%', height }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            innerRadius="60%"
            outerRadius="80%"
            paddingAngle={2}
            dataKey={dataKey}
            nameKey={nameKey}
            onMouseEnter={onPieEnter}
            onMouseLeave={onPieLeave}
            stroke="none"
          >
            {data.map((_, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={colors[index % colors.length]} 
                opacity={activeIndex === index || activeIndex === -1 ? 1 : 0.6}
                style={{ outline: 'none' }}
              />
            ))}
          </Pie>
          <Tooltip 
            contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
            formatter={(value: any) => [valueFormatter ? valueFormatter(value) : value]}
          />
          <Legend 
            layout="horizontal" 
            verticalAlign="bottom" 
            align="center"
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
