import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const RevenueTrend = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="empty-chart-state">No data available</div>;
  }

  return (
    <ResponsiveContainer width="100%" height="100%">
      <AreaChart
        data={data}
        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
      >
        <defs>
          <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid
          strokeDasharray="3 3"
          vertical={false}
          stroke="#f3f4f6"
        />
        <XAxis
          dataKey="order_date"
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#6b7280", fontSize: 12 }}
          dy={10}
        />
        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#6b7280", fontSize: 12 }}
          tickFormatter={(value) => `$${value}`}
        />
        <Tooltip
          contentStyle={{
            borderRadius: "8px",
            border: "none",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          }}
          formatter={(value) => [`$${value}`, "Revenue"]}
        />
        <Area
          type="monotone"
          dataKey="revenue"
          stroke="#2563eb"
          strokeWidth={3}
          fillOpacity={1}
          fill="url(#colorRevenue)"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default RevenueTrend;
