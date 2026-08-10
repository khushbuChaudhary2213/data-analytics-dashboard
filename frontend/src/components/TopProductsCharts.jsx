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

const TopProductsChart = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="empty-chart-state">No data available</div>;
  }

  const sortedData = [...data].sort((a, b) => b.revenue - a.revenue);

  const RANKING_COLORS = ["#3b82f6", "#6366f1", "#8b5cf6"];

  return (
    <ResponsiveContainer width="100%" height="100%">
      <BarChart
        data={sortedData}
        layout="vertical"
        margin={{ top: 10, right: 30, left: 10, bottom: 0 }}
        barSize={32}
      >
        <CartesianGrid
          strokeDasharray="3 3"
          horizontal={true}
          vertical={false}
          stroke="#f3f4f6"
        />

        <XAxis
          type="number"
          axisLine={false}
          tickLine={false}
          tickFormatter={(value) => `$${value}`}
          tick={{ fill: "#6b7280", fontSize: 12 }}
        />

        <YAxis
          dataKey="product_name"
          type="category"
          axisLine={false}
          tickLine={false}
          tick={{ fill: "#374151", fontSize: 13, fontWeight: 500 }}
          width={80} // Gives the product names enough room to breathe
        />

        <Tooltip
          cursor={{ fill: "#f3f4f6" }}
          contentStyle={{
            borderRadius: "8px",
            border: "none",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          }}
          formatter={(value) => [`$${value}`, "Revenue"]}
        />

        <Bar dataKey="revenue" radius={[0, 6, 6, 0]}>
          {sortedData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={RANKING_COLORS[index % RANKING_COLORS.length]}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  );
};

export default TopProductsChart;
