import { useEffect, useState } from "react";
import { BarChart, Bar, LineChart, Line, ResponsiveContainer, XAxis, YAxis, CartesianGrid, Tooltip, Legend, PieChart, Pie, Cell } from "recharts";
import api from "../services/api";

function IncidentManagement() {
  const [incidents, setIncidents] = useState<any[]>([]);
  const [selectedIncident, setSelectedIncident] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    fetchIncidents();
  }, [filter]);

  const fetchIncidents = async () => {
    try {
      const response = await api.get("/api/v1/incidents", {
        params: { status: filter === "all" ? undefined : filter },
      });
      setIncidents(response.data.data || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const statusCounts = incidents.reduce((acc: any, i: any) => {
    acc[i.status] = (acc[i.status] || 0) + 1;
    return acc;
  }, {});

  const statusData = Object.entries(statusCounts).map(([status, count]) => ({
    name: status,
    value: count,
  }));

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Incident Response</h2>
        <p className="mt-2 text-slate-400">Manage and track security incidents across your infrastructure.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-4">
        <div className="rounded-2xl border border-cyber-700 bg-cyber-800 p-4">
          <p className="text-sm text-slate-400">Total Incidents</p>
          <p className="mt-2 text-3xl font-bold text-cyan-300">{incidents.length}</p>
        </div>
        <div className="rounded-2xl border border-cyber-700 bg-cyber-800 p-4">
          <p className="text-sm text-slate-400">New</p>
          <p className="mt-2 text-3xl font-bold text-yellow-400">{statusCounts["new"] || 0}</p>
        </div>
        <div className="rounded-2xl border border-cyber-700 bg-cyber-800 p-4">
          <p className="text-sm text-slate-400">Investigating</p>
          <p className="mt-2 text-3xl font-bold text-orange-400">{statusCounts["investigating"] || 0}</p>
        </div>
        <div className="rounded-2xl border border-cyber-700 bg-cyber-800 p-4">
          <p className="text-sm text-slate-400">Closed</p>
          <p className="mt-2 text-3xl font-bold text-emerald-400">{statusCounts["closed"] || 0}</p>
        </div>
      </div>

      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-xl font-semibold text-cyan-100">Incident Distribution</h3>
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={statusData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={100} paddingAngle={3}>
                  {statusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={["#22d3ee", "#f59e0b", "#ef4444", "#10b981"][index % 4]} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: 14, border: "1px solid #334155" }} itemStyle={{ color: "#f8fafc" }} />
                <Legend verticalAlign="bottom" height={36} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-xl font-semibold text-cyan-100">Recent Incidents</h3>
          <div className="mt-4 space-y-3 max-h-96 overflow-y-auto">
            {incidents.slice(0, 8).map((incident) => (
              <div key={incident.id} className="cursor-pointer rounded-lg border border-cyber-600 bg-cyber-700/50 p-3 transition hover:bg-cyber-600" onClick={() => setSelectedIncident(incident)}>
                <p className="font-semibold text-cyan-200">{incident.title}</p>
                <div className="mt-2 flex justify-between text-xs text-slate-400">
                  <span className="rounded bg-cyber-600 px-2 py-1">{incident.status}</span>
                  <span className="text-orange-300">Risk: {incident.risk_score}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {selectedIncident && (
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-xl font-semibold text-cyan-100">Incident Details</h3>
          <div className="mt-4 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-slate-400">Title</p>
              <p className="mt-1 text-lg font-semibold text-white">{selectedIncident.title}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Status</p>
              <p className="mt-1 text-lg font-semibold text-cyan-300">{selectedIncident.status}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Severity</p>
              <p className="mt-1 text-lg font-semibold text-red-400">{selectedIncident.severity}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Risk Score</p>
              <p className="mt-1 text-lg font-semibold text-orange-300">{selectedIncident.risk_score}</p>
            </div>
            <div className="col-span-2">
              <p className="text-sm text-slate-400">Description</p>
              <p className="mt-2 text-white">{selectedIncident.description}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default IncidentManagement;
