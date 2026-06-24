import { NavLink } from "react-router-dom";

const navItems = [
  { label: "Dashboard", path: "/", icon: "📊" },
  { label: "Threats", path: "/threats", icon: "🛡️" },
  { label: "Alerts", path: "/alerts", icon: "🚨" },
  { label: "Incidents", path: "/incidents", icon: "🔴" },
  { label: "Reports", path: "/reports", icon: "📋" },
  { label: "Analytics", path: "/analytics", icon: "📈" },
  { label: "Threat Intelligence", path: "/threat-intelligence", icon: "🎯" },
  { label: "IOC Center", path: "/ioc-center", icon: "🔍" },
  { label: "Threat Hunting", path: "/threat-hunting", icon: "🦅" },
  { label: "MITRE ATT&CK", path: "/mitre", icon: "🗂️" },
  { label: "Audit Logs", path: "/audit-logs", icon: "📝" },
  { label: "User Management", path: "/users", icon: "👥" },
  { label: "Settings", path: "/settings", icon: "⚙️" },
];

function Sidebar() {
  return (
    <aside className="h-screen w-full border-b border-cyber-700 bg-cyber-900 lg:w-80 lg:border-r lg:border-b-0 overflow-y-auto">
      <div className="mx-auto flex max-w-7xl flex-col px-4 py-6 sm:px-6">
        <div className="mb-8 flex items-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-cyan-500 to-blue-600 shadow-glow" />
          <div>
            <p className="text-sm uppercase tracking-[0.3em] text-cyan-300 font-bold">NetSentinel</p>
            <p className="text-xs text-slate-500">Enterprise SOC</p>
          </div>
        </div>
        <nav className="space-y-1 flex-1">
          {navItems.map((item) => (
            <NavLink
              to={item.path}
              key={item.label}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-2xl px-4 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-cyber-700 text-cyan-200 shadow-glow"
                    : "text-slate-300 hover:bg-cyber-800 hover:text-white"
                }`
              }
            >
              <span className="text-lg">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
      </div>
    </aside>
  );
}

export default Sidebar;\n
