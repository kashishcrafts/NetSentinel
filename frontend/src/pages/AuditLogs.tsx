import { useEffect, useState } from "react";
import api from "../services/api";

function AuditLogs() {
  const [logs, setLogs] = useState<any[]>([]);
  const [filter, setFilter] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAuditLogs();
  }, [filter]);

  const fetchAuditLogs = async () => {
    try {
      const response = await api.get("/api/v1/audit-logs");
      setLogs(response.data.data || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const getActionColor = (action: string) => {
    const colors: any = {
      CREATE: "text-emerald-400",
      UPDATE: "text-blue-400",
      DELETE: "text-red-400",
      ASSIGN: "text-purple-400",
      RESOLVE: "text-cyan-400",
      ESCALATE: "text-orange-400",
    };
    return colors[action] || "text-slate-400";
  };

  const getActionBg = (action: string) => {
    const colors: any = {
      CREATE: "bg-emerald-900",
      UPDATE: "bg-blue-900",
      DELETE: "bg-red-900",
      ASSIGN: "bg-purple-900",
      RESOLVE: "bg-cyan-900",
      ESCALATE: "bg-orange-900",
    };
    return colors[action] || "bg-gray-900";
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Audit Logs</h2>
        <p className="mt-2 text-slate-400">Track all system activities and changes.</p>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["all", "CREATE", "UPDATE", "DELETE", "ASSIGN", "RESOLVE"].map((action) => (
          <button
            key={action}
            onClick={() => setFilter(action)}
            className={`rounded-full px-4 py-2 transition ${
              filter === action ? "bg-cyan-600 text-white" : "border border-cyber-700 text-slate-400 hover:text-white"
            }`}
          >
            {action}
          </button>
        ))}
      </div>

      <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
        <h3 className="text-lg font-semibold text-cyan-100 mb-4">Activity Log</h3>
        <div className="overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-cyber-700 text-slate-300">
              <tr>
                <th className="px-4 py-3">Timestamp</th>
                <th className="px-4 py-3">User</th>
                <th className="px-4 py-3">Action</th>
                <th className="px-4 py-3">Entity</th>
                <th className="px-4 py-3">IP Address</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-700">
              {logs.slice(0, 50).map((log) => (
                <tr key={log.id} className="hover:bg-cyber-700/50">
                  <td className="px-4 py-3 text-slate-400 text-xs">{new Date(log.timestamp).toLocaleString()}</td>
                  <td className="px-4 py-3 text-white">User #{log.user_id}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded px-2 py-1 text-xs font-semibold ${getActionBg(log.action)} ${getActionColor(log.action)}`}>{log.action}</span>
                  </td>
                  <td className="px-4 py-3 text-slate-300">
                    {log.entity_type} #{log.entity_id}
                  </td>
                  <td className="px-4 py-3 font-mono text-xs text-slate-400">{log.ip_address || "—"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AuditLogs;
