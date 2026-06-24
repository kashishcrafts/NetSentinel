type Alert = {
  id: number;
  alert_type: string;
  status: string;
  priority: number;
  message: string;
  assigned_to?: number;
  is_read: boolean;
  created_at: string;
};

type AlertTableProps = {
  alerts: Alert[];
};

function AlertTable({ alerts }: AlertTableProps) {
  return (
    <div className="overflow-hidden rounded-3xl border border-cyber-700 bg-cyber-800 shadow-glow">
      <table className="min-w-full divide-y divide-cyber-700 text-left text-sm text-slate-200">
        <thead className="bg-cyber-900">
          <tr>
            <th className="px-6 py-4">Alert</th>
            <th className="px-6 py-4">Status</th>
            <th className="px-6 py-4">Priority</th>
            <th className="px-6 py-4">Assigned</th>
            <th className="px-6 py-4">Read</th>
            <th className="px-6 py-4">Created</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-cyber-700 bg-cyber-800">
          {alerts.map((alert) => (
            <tr key={alert.id} className="hover:bg-cyber-900/80">
              <td className="px-6 py-4 font-semibold text-slate-100">{alert.alert_type}</td>
              <td className="px-6 py-4 text-cyan-300">{alert.status}</td>
              <td className="px-6 py-4 text-slate-200">{alert.priority}</td>
              <td className="px-6 py-4 text-slate-300">{alert.assigned_to ?? "Unassigned"}</td>
              <td className="px-6 py-4 text-slate-300">{alert.is_read ? "Yes" : "No"}</td>
              <td className="px-6 py-4 text-slate-400">{new Date(alert.created_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default AlertTable;
