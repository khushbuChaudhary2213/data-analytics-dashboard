import { useState } from "react";
import { LayoutDashboard, Menu, X, PanelLeft } from "lucide-react";

function Sidebar() {
  const [isMobileOpen, setIsMobileOpen] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <>
      {!isMobileOpen && (
        <button
          className="mobile-menu-button"
          onClick={() => setIsMobileOpen(true)}
          aria-label="Open sidebar"
        >
          <Menu size={20} />
        </button>
      )}

      <aside
        className={`sidebar ${
          isExpanded ? "sidebar-expanded" : ""
        } ${isMobileOpen ? "sidebar-mobile-open" : ""}`}
      >
        <div className="sidebar-header">
          <span className="sidebar-logo">InsightsFlow</span>

          <button
            className="sidebar-toggle"
            onClick={() => setIsExpanded((prev) => !prev)}
            aria-label="Toggle sidebar"
          >
            <PanelLeft size={20} />
          </button>

          <button
            className="sidebar-close-button"
            onClick={() => setIsMobileOpen(false)}
            aria-label="Close sidebar"
          >
            <X size={22} />
          </button>
        </div>

        <nav className="sidebar-nav">
          <a
            href="/dashboard"
            className="nav-item"
            onClick={() => setIsMobileOpen(false)}
          >
            <LayoutDashboard size={20} />
            <span className="nav-label">Dashboard</span>
          </a>
        </nav>
      </aside>

      {isMobileOpen && (
        <div
          className="sidebar-overlay"
          onClick={() => setIsMobileOpen(false)}
        />
      )}
    </>
  );
}

export default Sidebar;
