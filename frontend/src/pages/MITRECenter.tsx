import { useEffect, useState } from "react";
import api from "../services/api";

const TACTICS = [
  { id: "TA0001", name: "Initial Access" },
  { id: "TA0002", name: "Execution" },
  { id: "TA0003", name: "Persistence" },
  { id: "TA0004", name: "Privilege Escalation" },
  { id: "TA0005", name: "Defense Evasion" },
  { id: "TA0006", name: "Credential Access" },
  { id: "TA0007", name: "Discovery" },
  { id: "TA0008", name: "Lateral Movement" },
  { id: "TA0009", name: "Collection" },
  { id: "TA0010", name: "Exfiltration" },
  { id: "TA0011", name: "Command and Control" },
  { id: "TA0040", name: "Impact" },
];

function MITRECenter() {
  const [selectedTactic, setSelectedTactic] = useState("TA0001");
  const [tacticsData, setTacticsData] = useState<any[]>([]);
  const [threatMap, setThreatMap] = useState<any>(null);

  useEffect(() => {
    fetchAttackMatrix();
    fetchTacticDetails(selectedTactic);
  }, [selectedTactic]);

  const fetchAttackMatrix = async () => {
    try {
      const response = await api.get("/api/v1/mitre/attack-matrix");
      setThreatMap(response.data.matrix);
    } catch (error) {
      console.error(error);
    }
  };

  const fetchTacticDetails = async (tacticId: string) => {
    try {
      const response = await api.get(`/api/v1/mitre/tactic/${tacticId}`);
      setTacticsData([response.data]);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">MITRE ATT&CK Navigator</h2>
        <p className="mt-2 text-slate-400">Map threats to MITRE ATT&CK tactics and techniques.</p>
      </div>

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2 rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-lg font-semibold text-cyan-100">Tactics Matrix</h3>
          <div className="mt-4 grid grid-cols-2 gap-2 md:grid-cols-3">
            {TACTICS.map((tactic) => (
              <button
                key={tactic.id}
                onClick={() => setSelectedTactic(tactic.id)}
                className={`rounded-lg p-3 text-center text-sm transition ${
                  selectedTactic === tactic.id
                    ? "bg-cyan-600 text-white"
                    : "border border-cyber-700 text-slate-300 hover:text-white"
                }`}
              >
                <p className="font-mono text-xs">{tactic.id}</p>
                <p className="mt-1 font-semibold">{tactic.name}</p>
              </button>
            ))}
          </div>
        </div>

        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-lg font-semibold text-cyan-100">Threat Coverage</h3>
          {threatMap && (
            <div className="mt-4 space-y-2">
              {Object.entries(threatMap).slice(0, 6).map(([tacticId, tacticData]: any) => (
                <div key={tacticId} className="flex justify-between rounded bg-cyber-700 p-2 text-xs">
                  <span className="text-slate-400">{tacticData.name}</span>
                  <span className="font-bold text-cyan-300">{tacticData.threat_count}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {tacticsData.length > 0 && (
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-lg font-semibold text-cyan-100">{tacticsData[0].tactic_name}</h3>
          <p className="mt-2 text-slate-400">{tacticsData[0].tactic_id}</p>

          <div className="mt-4 space-y-3">
            <div>
              <h4 className="text-sm font-semibold text-cyan-200">Techniques</h4>
              <div className="mt-2 flex flex-wrap gap-2">
                {tacticsData[0].techniques.map((tech: string) => (
                  <span key={tech} className="rounded bg-cyber-700 px-3 py-1 text-xs font-mono text-cyan-300">
                    {tech}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-semibold text-cyan-200">Mapped Threats ({tacticsData[0].mapped_threats?.length || 0})</h4>
              <div className="mt-2 max-h-40 space-y-1 overflow-y-auto">
                {tacticsData[0].mapped_threats?.map((threat: any) => (
                  <div key={threat.id} className="rounded bg-cyber-700/50 p-2 text-sm text-slate-300">
                    {threat.name}
                  </div>
                )) || <p className="text-slate-500">No mapped threats</p>}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default MITRECenter;
