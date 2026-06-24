import { Link } from "react-router-dom";

function NotFound() {
  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-3xl flex-col items-center justify-center px-4 py-10 text-center">
      <div className="rounded-3xl border border-cyber-700 bg-cyber-900/95 p-10 shadow-glow">
        <h2 className="text-3xl font-semibold text-cyan-200">Page Not Found</h2>
        <p className="mt-4 text-slate-400">The route you requested does not exist.</p>
        <Link to="/" className="mt-6 inline-flex rounded-full bg-cyber-500 px-6 py-3 text-sm font-semibold text-slate-900 transition hover:bg-cyan-400">
          Return Home
        </Link>
      </div>
    </div>
  );
}

export default NotFound;
