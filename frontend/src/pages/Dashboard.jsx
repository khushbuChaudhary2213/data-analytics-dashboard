import {
  DollarSign,
  ShoppingCart,
  TrendingUp,
  AlertTriangle,
  IndianRupee,
  Euro,
  PoundSterling,
} from "lucide-react";
import KPICard from "../components/KpiCard";
import RevenueTrend from "../components/RevenueTrend";
import DeliveryPerformance from "../components/DeliveryPerformance";
import CategoryRevenue from "../components/CategoryRevenue";
import TopProductsChart from "../components/TopProductsCharts";
import { useState } from "react";

const currencySymbols = {
  INR: "₹",
  USD: "$",
  EUR: "€",
  GBP: "£",
};

const currencyIcons = {
  INR: IndianRupee,
  USD: DollarSign,
  EUR: Euro,
  GBP: PoundSterling,
};

function Dashboard({ summaryData, loading }) {
  const [view, setView] = useState("revenue");
  const currency = summaryData?.currency || "INR";

  const symbol = currencySymbols[currency] || currency;
  const CurrencyIcon = currencyIcons[currency] || IndianRupee;

  return (
    <div className="dashboard-body">
      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
        </div>
      ) : (
        <div className="content-wrapper">
          <div className="kpi-grid">
            <KPICard
              title="Total Revenue"
              value={`${symbol}${summaryData?.kpis?.total_revenue?.toLocaleString() || 0}`}
              icon={<CurrencyIcon size={24} />}
              color="blue"
            />
            <KPICard
              title="Total Orders"
              value={summaryData?.kpis?.total_orders || 0}
              icon={<ShoppingCart size={24} />}
              color="green"
            />
            <KPICard
              title="Avg Order Value"
              value={`${symbol}${summaryData?.kpis?.average_order_value?.toLocaleString() || 0}`}
              icon={<TrendingUp size={24} />}
              color="purple"
            />
            <KPICard
              title="Delayed Orders"
              value={summaryData?.kpis?.delayed_orders || 0}
              icon={<AlertTriangle size={20} />}
              color="red"
            />
          </div>

          <div className="charts-grid">
            <div className="chart-card-large">
              <div className="chart-header-flex">
                <h3 className="chart-title">
                  {view === "revenue" ? "Revenue Trend" : "Orders Trend"}
                </h3>

                <div className="view-toggle">
                  <button
                    className={view === "revenue" ? "active" : ""}
                    onClick={() => setView("revenue")}
                  >
                    Revenue
                  </button>

                  <button
                    className={view === "orders" ? "active" : ""}
                    onClick={() => setView("orders")}
                  >
                    Orders
                  </button>
                </div>
              </div>

              <div className="chart-container">
                <RevenueTrend
                  symbol={symbol}
                  data={summaryData?.revenue_trend}
                  view={view}
                />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header-flex">
                <h3 className="chart-title" style={{ marginBottom: 0 }}>
                  Delivery Status
                </h3>
                <span className="chart-badge">
                  Avg:{" "}
                  {summaryData?.delivery_performance?.average_delivery_days?.toFixed(
                    1,
                  )}{" "}
                  Days
                </span>
              </div>
              <div className="chart-container">
                <DeliveryPerformance
                  data={summaryData?.delivery_performance?.status_counts}
                />
              </div>
            </div>
          </div>

          <div className="charts-grid">
            <div className="chart-card-large">
              <h3 className="chart-title">Revenue by Category</h3>
              <div className="chart-container-large">
                <CategoryRevenue
                  symbol={symbol}
                  data={summaryData?.category_revenue}
                />
              </div>
            </div>

            <div className="chart-card">
              <h3 className="chart-title">Top Products</h3>
              <div className="chart-container-large">
                <TopProductsChart
                  symbol={symbol}
                  data={summaryData?.top_products}
                />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
