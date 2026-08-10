import { DollarSign, ShoppingCart, TrendingUp } from "lucide-react";
import KPICard from "../components/KpiCard";
import RevenueTrend from "../components/RevenueTrend";
import DeliveryPerformance from "../components/DeliveryPerformance";
import CategoryRevenue from "../components/CategoryRevenue";
import TopProductsChart from "../components/TopProductsCharts";

const currencySymbols = {
  INR: "₹",
  USD: "$",
  EUR: "€",
  GBP: "£",
};

function Dashboard({ summaryData, loading }) {
  const currency = summaryData?.currency || "INR";

  const symbol = currencySymbols[currency] || currency;

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
              icon={<DollarSign size={24} />}
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
          </div>

          <div className="charts-grid">
            <div className="chart-card-large">
              <h3 className="chart-title">Revenue Trend</h3>
              <div className="chart-container">
                <RevenueTrend data={summaryData?.revenue_trend} />
              </div>
            </div>

            <div className="chart-card">
              <div className="chart-header-flex">
                <h3 className="chart-title" style={{ marginBottom: 0 }}>
                  Delivery Status
                </h3>
                <span className="chart-badge">
                  Avg:
                  {summaryData?.delivery_performance?.average_delivery_days?.toFixed(
                    0,
                  )}
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
                <CategoryRevenue data={summaryData?.category_revenue} />
              </div>
            </div>

            <div className="chart-card">
              <h3 className="chart-title">Top Products</h3>
              <div className="chart-container-large">
                <TopProductsChart data={summaryData?.top_products} />
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;
