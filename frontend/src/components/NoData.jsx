import { FileSearch } from "lucide-react";

function NoData({ message, onReset }) {
  return (
    <div className="no-data">
      <div className="no-data-icon">
        <FileSearch size={40} />
      </div>

      <h2>No Data Found</h2>

      <p>{message || "No records match your selected filters."}</p>

      <button onClick={onReset}>Reset Filters</button>
    </div>
  );
}

export default NoData;
