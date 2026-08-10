import React from "react";

const KPICard = ({ title, value, icon, color }) => {
  return (
    <div className={`kpi-card ${color}`}>
      <div>
        <p className="kpi-title">{title}</p>
        <p className="kpi-value">{value}</p>
      </div>
      <div className="kpi-icon-wrapper"> {icon} </div>
    </div>
  );
};

export default KPICard;
