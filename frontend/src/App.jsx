import { useEffect, useState } from "react";
import api from "./utils/axios";
import "./index.css";

import Header from "./components/Header";
import Dashboard from "./pages/Dashboard";
import Sidebar from "./components/Sidebar";
import Filters from "./components/Filters";

function App() {
  const [filters, setFilters] = useState({
    category: "All",
    status: "All",
    start_date: "",
    end_date: "",
    currency: "INR",
  });

  const [summaryData, setSummaryData] = useState(null);
  const [initialData, setInitialData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async (currentFilters = filters) => {
    setLoading(true);
    setError(null);
    try {
      const queryParams = new URLSearchParams();

      if (currentFilters.category && currentFilters.category !== "All") {
        queryParams.append("category", currentFilters.category);
      }
      if (currentFilters.status && currentFilters.status !== "All") {
        queryParams.append("status", currentFilters.status);
      }

      if (currentFilters.start_date) {
        queryParams.append("start_date", currentFilters.start_date);
      }

      if (currentFilters.end_date) {
        queryParams.append("end_date", currentFilters.end_date);
      }
      if (currentFilters.currency) {
        queryParams.append("currency", currentFilters.currency);
      }

      const query = queryParams.toString();
      const url = query ? `/analytics/summary?${query}` : "/analytics/summary";

      const res = await api.get(url);

      if (res.statusText !== "OK") {
        throw new Error("Failed to fetch the summary");
      }

      setSummaryData(res.data);

      if (!initialData) setInitialData(res.data);
    } catch (err) {
      setError(
        err.response?.data?.message || err.message || "Something went wrong",
      );
      console.err(err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyFilters = (newFilters) => {
    setFilters(newFilters);
    fetchAnalytics(newFilters);
  };

  const handleResetFilters = () => {
    const resetFilters = {
      category: "All",
      status: "All",
      start_date: "",
      end_date: "",
      currency: "INR",
    };

    setFilters(resetFilters);
    fetchAnalytics(resetFilters);
  };

  const categories =
    initialData?.category_revenue?.map((item) => item.category) || [];

  const statuses =
    initialData?.delivery_performance?.status_counts?.map(
      (item) => item.status,
    ) || [];

  if (error && !summaryData)
    return (
      <div className="error-message">Error loading dashboard: {error}</div>
    );

  return (
    <div className="app-container">
      <Sidebar />
      <main className="main-content">
        <Header />
        <Filters
          categories={categories}
          statuses={statuses}
          onApply={handleApplyFilters}
          onReset={handleResetFilters}
        />
        <Dashboard summaryData={summaryData} loading={loading} />
      </main>
    </div>
  );
}

export default App;
