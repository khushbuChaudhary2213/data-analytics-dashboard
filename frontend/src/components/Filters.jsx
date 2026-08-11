import { useState } from "react";

function Filters({ categories, statuses, onApply, onReset }) {
  const [category, setCategory] = useState("All");
  const [status, setStatus] = useState("All");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [currency, setCurrency] = useState("INR");

  const isDefaultFilters =
    category === "All" &&
    status === "All" &&
    startDate === "" &&
    endDate === "" &&
    currency === "INR";

  const handleApply = () => {
    if (isDefaultFilters) return;

    onApply({
      category,
      status,
      start_date: startDate,
      end_date: endDate,
      currency,
    });
  };

  const handleReset = () => {
    if (isDefaultFilters) return;

    setCategory("All");
    setStatus("All");
    setStartDate("");
    setEndDate("");
    setCurrency("INR");

    onReset();
  };

  return (
    <div className="filters">
      <div className="filter-group">
        <label>From</label>

        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>To</label>

        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label>Category</label>

        <select value={category} onChange={(e) => setCategory(e.target.value)}>
          <option value="All">All</option>

          {categories.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-group">
        <label>Status</label>

        <select value={status} onChange={(e) => setStatus(e.target.value)}>
          <option value="All">All</option>

          {statuses.map((status) => (
            <option key={status} value={status}>
              {status}
            </option>
          ))}
        </select>
      </div>
      <div className="filter-group">
        <label>Currency</label>

        <select value={currency} onChange={(e) => setCurrency(e.target.value)}>
          <option value="INR">INR (₹)</option>
          <option value="USD">USD ($)</option>
          <option value="EUR">EUR (€)</option>
          <option value="GBP">GBP (£)</option>
        </select>
      </div>

      <div className="filter-buttons">
        <button onClick={handleApply}>Apply</button>

        <button onClick={handleReset}>Reset</button>
      </div>
    </div>
  );
}

export default Filters;
