import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

const CategoryRevenue = ({ symbol, data }) => {
  if (!data || data.length === 0) {
    return <div className="empty-chart-state">No data available</div>;
  }

  const COLORS = ["#10b981", "#f59e0b", "#6366f1", "#ec4899", "#8b5cf6"];

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={data}
        margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        barSize={40}
      >
        <CartesianGrid
          strokeDasharray="3 3"
          vertical={false}
          stroke="#c5c5c5"
        />
        <XAxis
          dataKey="category"
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#6b7280", fontSize: 12 }}
          dy={10}
        />
        <YAxis
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#6b7280", fontSize: 12 }}
          tickFormatter={(value) => `${symbol}${value}`}
        />
        <Tooltip
          cursor={{ fill: "#f3f4f6" }}
          contentStyle={{
            borderRadius: "8px",
            border: "none",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          }}
          formatter={(value) => [`${symbol}${value}`, "Revenue"]}
        />
        <Bar dataKey="revenue" radius={[6, 6, 0, 0]}>
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default CategoryRevenue;
