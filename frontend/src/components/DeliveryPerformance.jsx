import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const DeliveryPerformance = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="empty-chart-state">No data available</div>;
  }

  const getStatusColor = (status) => {
    if (status.toLowerCase() === "delivered") return "#10b981"; // Green
    if (status.toLowerCase() === "delayed") return "#ef4444"; // Red
    return "#6b7280"; // Gray fallback
  };

  return (
    <ResponsiveContainer width="100%" height="100%">
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={50}
          outerRadius={90}
          dataKey="count"
          nameKey="status"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={getStatusColor(entry.status)} />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            borderRadius: "8px",
            border: "none",
            boxShadow: "0 4px 6px -1px rgb(0 0 0 / 0.1)",
          }}
        />
        <Legend
          verticalAlign="bottom"
          height={36}
          iconType="circle"
          formatter={(value) => (
            <span className="chart-legend-text">{value}</span>
          )}
        />
      </PieChart>
    </ResponsiveContainer>
  );
};

export default DeliveryPerformance;
