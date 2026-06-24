type Threat = {
  id: number;
  threat_name: string;
  threat_type: string;
  severity: string;
  source_ip?: string;
  destination_ip?: string;
  confidence_score: number;
  detected_at: string;
};

type ThreatTableProps = {
  threats: Threat[];
};

function ThreatTable({ threats }: ThreatTableProps) {
  return (
    <div className="overflow-hidden rounded-3xl border border-cyber-700 bg-cyber-800 shadow-glow">
      <table className="min-w-full divide-y divide-cyber-700 text-left text-sm text-slate-200">
        <thead className="bg-cyber-900">
          <tr>
            <th className="px-6 py-4">Threat</th>
            <th className="px-6 py-4">Type</th>
            <th className="px-6 py-4">Severity</th>
            <th className="px-6 py-4">Source</th>
            <th className="px-6 py-4">Destination</th>
            <th className="px-6 py-4">Confidence</th>
            <th className="px-6 py-4">Detected</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-cyber-700 bg-cyber-800">
          {threats.map((threat) => (
            <tr key={threat.id} className="hover:bg-cyber-900/80">
              <td className="px-6 py-4 font-semibold text-slate-100">{threat.threat_name}</td>
              <td className="px-6 py-4 text-slate-300">{threat.threat_type}</td>
              <td className="px-6 py-4 text-cyan-300">{threat.severity}</td>
              <td className="px-6 py-4 text-slate-300">{threat.source_ip ?? "-"}</td>
              <td className="px-6 py-4 text-slate-300">{threat.destination_ip ?? "-"}</td>
              <td className="px-6 py-4 text-slate-200">{(threat.confidence_score * 100).toFixed(0)}%</td>
              <td className="px-6 py-4 text-slate-400">{new Date(threat.detected_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ThreatTable;
