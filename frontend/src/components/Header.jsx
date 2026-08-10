import { User, Filter } from "lucide-react";
import ThemeToggle from "./ThemeToggle";

function Header({ onF }) {
  return (
    <header className="top-header">
      <h1 className="header-title">Analytics Overview</h1>

      <div className="header-actions">
        <div className="header-user">
          <span>User</span>

          <div className="user-icon">
            <User size={18} />
          </div>
        </div>
        <ThemeToggle />
      </div>
    </header>
  );
}

export default Header;
