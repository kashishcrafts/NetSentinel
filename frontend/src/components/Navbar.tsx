import { Link } from "react-router-dom";

function Navbar() {
  return (
    <header className="sticky top-0 z-20 border-b border-cyber-700 bg-cyber-900/95 backdrop-blur-sm">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6">
        <div>
          <h1 className="text-lg font-semibold tracking-wide text-cyan-300">NetSentinel</h1>
          <p className="text-sm text-slate-400">Cyber Threat Intelligence Platform</p>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/analytics" className="rounded-full border border-cyber-700 px-4 py-2 text-sm text-cyan-200 transition hover:border-cyan-300 hover:text-white">
            Analytics
          </Link>
          <button
            onClick={() => {
              localStorage.removeItem("netsentinel_token");
              window.location.href = "/login";
            }}
            className="rounded-full bg-cyber-500 px-4 py-2 text-sm font-semibold text-slate-900 transition hover:bg-cyan-400"
          >
            Logout
          </button>
        </div>
      </div>
    </header>
  );
}

export default Navbar;
