type DashboardCardProps = {
  label: string;
  value: number;
  icon: string;
  accent: string;
};

function DashboardCard({ label, value, icon, accent }: DashboardCardProps) {
  return (
    <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow transition hover:-translate-y-0.5">
      <div className="flex items-center justify-between">
        <span className={`rounded-2xl px-3 py-2 text-sm font-semibold text-slate-900 ${accent}`}>{icon}</span>
        <p className="text-xs uppercase tracking-[0.3em] text-slate-500">{label}</p>
      </div>
      <p className="mt-6 text-4xl font-semibold text-cyan-200">{value.toLocaleString()}</p>
    </div>
  );
}

export default DashboardCard;
