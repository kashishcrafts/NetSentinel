import { useState } from "react";
import api from "../services/api";

function ThreatHunting() {
  const [searchType, setSearchType] = useState<"ip" | "domain" | "hash">("ip");
  const [searchValue, setSearchValue] = useState("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!searchValue.trim()) return;
    setLoading(true);

    try {
      let response;
      if (searchType === "ip") {
        response = await api.post("/api/v1/threat-hunting/search-ip", {}, { params: { ip: searchValue } });
      } else if (searchType === "domain") {
        response = await api.post("/api/v1/threat-hunting/search-domain", {}, { params: { domain: searchValue } });
      } else if (searchType === "hash") {
        response = await api.post("/api/v1/threat-hunting/search-hash", {}, { params: { file_hash: searchValue } });
      }
      setResults(response?.data);
    } catch (error) {
      console.error(error);
      setResults({ error: "Search failed" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Threat Hunting</h2>
        <p className="mt-2 text-slate-400">Proactive threat hunting across your infrastructure.</p>
      </div>

      <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
        <h3 className="text-lg font-semibold text-cyan-100">Hunt by Indicator</h3>

        <div className="mt-4 flex gap-3 flex-wrap">
          {(["ip", "domain", "hash"] as const).map((type) => (
            <button
              key={type}
              onClick={() => setSearchType(type)}
              className={`rounded-full px-4 py-2 transition ${
                searchType === type ? "bg-cyan-600 text-white" : "border border-cyber-700 text-slate-400 hover:text-white"
              }`}
            >
              {type === "ip" ? "🔍 IP Address" : type === "domain" ? "🌐 Domain" : "🔗 File Hash"}
            </button>
          ))}
        </div>

        <div className="mt-4 flex gap-3">
          <input
            type="text"
            placeholder={searchType === "ip" ? "Enter IP address..." : searchType === "domain" ? "Enter domain..." : "Enter file hash..."}
            value={searchValue}
            onChange={(e) => setSearchValue(e.target.value)}
            onKeyPress={(e) => e.key === "Enter" && handleSearch()}
            className="flex-1 rounded-full border border-cyber-700 bg-cyber-700 px-4 py-3 text-white outline-none focus:border-cyan-400"
          />
          <button onClick={handleSearch} disabled={loading} className="rounded-full bg-cyan-600 px-6 py-3 font-semibold text-white hover:bg-cyan-500 disabled:opacity-50">
            {loading ? "Hunting..." : "Hunt"}
          </button>
        </div>
      </div>

      {results && (
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-lg font-semibold text-cyan-100">Hunting Results</h3>

          {results.error ? (
            <p className="mt-4 text-red-400">{results.error}</p>
          ) : (
            <div className="mt-4 space-y-4">
              {searchType === "ip" && (
                <>
                  <div className="grid gap-4 md:grid-cols-3">
                    <div className="rounded-lg bg-cyber-700 p-4">
                      <p className="text-sm text-slate-400">Total Flows</p>
                      <p className="mt-2 text-2xl font-bold text-cyan-300">{results.total_flows}</p>
                    </div>
                    <div className="rounded-lg bg-cyber-700 p-4">
                      <p className="text-sm text-slate-400">Suspicious Flows</p>
                      <p className="mt-2 text-2xl font-bold text-orange-400">{results.suspicious_flows}</p>
                    </div>
                    <div className="rounded-lg bg-cyber-700 p-4">
                      <p className="text-sm text-slate-400">Suspicious %</p>
                      <p className="mt-2 text-2xl font-bold text-red-400">
                        {results.total_flows > 0 ? ((results.suspicious_flows / results.total_flows) * 100).toFixed(1) : 0}%
                      </p>
                    </div>
                  </div>

                  <div>
                    <h4 className="text-sm font-semibold text-cyan-200">Suspicious Flows</h4>
                    <div className="mt-2 max-h-96 space-y-2 overflow-y-auto">
                      {results.flows?.map((flow: any, idx: number) => (
                        <div key={idx} className="rounded border border-cyber-600 bg-cyber-700/50 p-3">
                          <div className="flex justify-between text-sm">
                            <span className="text-slate-300">
                              {flow.source_ip} → {flow.destination_ip}
                            </span>
                            <span className="text-cyan-300">{flow.protocol}</span>
                          </div>
                          <div className="mt-2 flex justify-between text-xs text-slate-400">
                            <span>Anomaly: {(flow.anomaly_score * 100).toFixed(0)}%</span>
                            <span>Risk: {flow.risk_score.toFixed(1)}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </>
              )}

              {searchType === "domain" && (
                <div>
                  <p className="text-slate-300">Found {results.ioc_count} indicators for this domain</p>
                  <div className="mt-3 space-y-2">
                    {results.iocs?.map((ioc: any) => (
                      <div key={ioc.id} className="rounded border border-cyber-600 bg-cyber-700/50 p-3 text-sm">
                        <p className="text-cyan-200 font-mono">{ioc.value}</p>
                        <div className="mt-1 flex gap-4 text-xs text-slate-400">
                          <span>Type: {ioc.type}</span>
                          <span>Risk: {ioc.risk_score}</span>
                          <span>Reputation: {ioc.reputation}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {searchType === "hash" && (
                <div>
                  {results.found ? (
                    <div className="space-y-3 rounded border border-red-700 bg-red-900/20 p-4">
                      <p className="text-red-400 font-semibold">⚠️ Hash found in malware database!</p>
                      <div className="space-y-2 text-sm text-slate-300">
                        <p>
                          <span className="text-slate-400">Risk Score:</span> <span className="text-orange-300 font-bold">{results.risk_score}</span>
                        </p>
                        <p>
                          <span className="text-slate-400">Reputation:</span> <span className="text-orange-300 font-bold">{results.reputation}</span>
                        </p>
                        {results.description && (
                          <p>
                            <span className="text-slate-400">Description:</span> <span className="text-white">{results.description}</span>
                          </p>
                        )}
                      </div>
                    </div>
                  ) : (
                    <p className="text-emerald-400">✓ Hash not found in database</p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default ThreatHunting;
