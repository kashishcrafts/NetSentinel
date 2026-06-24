import { useEffect, useState } from "react";
import api from "../services/api";

function IOCCenter() {
  const [iocs, setIocs] = useState<any[]>([]);
  const [search, setSearch] = useState("");
  const [iocType, setIocType] = useState("all");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchIOCs();
  }, [iocType]);

  const fetchIOCs = async () => {
    try {
      const response = await api.get("/api/v1/iocs", {
        params: { ioc_type: iocType === "all" ? undefined : iocType },
      });
      setIocs(response.data.data || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async () => {
    if (!search.trim()) return;
    try {
      const response = await api.get("/api/v1/iocs/search", {
        params: { query: search },
      });
      setIocs(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  const getTypeColor = (type: string) => {
    const colors: any = {
      ip: "bg-blue-900 text-blue-300",
      domain: "bg-purple-900 text-purple-300",
      url: "bg-green-900 text-green-300",
      hash: "bg-orange-900 text-orange-300",
      email: "bg-pink-900 text-pink-300",
      file: "bg-yellow-900 text-yellow-300",
    };
    return colors[type] || "bg-gray-900 text-gray-300";
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">IOC Management Center</h2>
        <p className="mt-2 text-slate-400">Search, manage, and track indicators of compromise.</p>
      </div>

      <div className="flex gap-3">
        <input
          type="text"
          placeholder="Search IOCs..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="flex-1 rounded-full border border-cyber-700 bg-cyber-800 px-4 py-2 text-white outline-none focus:border-cyan-400"
        />
        <button onClick={handleSearch} className="rounded-full bg-cyan-600 px-6 py-2 font-semibold text-white hover:bg-cyan-500">
          Search
        </button>
      </div>

      <div className="flex gap-2 flex-wrap">
        {["all", "ip", "domain", "url", "hash", "email", "file"].map((type) => (
          <button
            key={type}
            onClick={() => setIocType(type)}
            className={`rounded-full px-4 py-2 transition ${iocType === type ? "bg-cyan-600 text-white" : "border border-cyber-700 text-slate-400 hover:text-white"}`}
          >
            {type.toUpperCase()}
          </button>
        ))}
      </div>

      <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
        <h3 className="text-lg font-semibold text-cyan-100">IOCs ({iocs.length})</h3>
        <div className="mt-4 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="border-b border-cyber-700 text-slate-300">
              <tr>
                <th className="px-4 py-3">Value</th>
                <th className="px-4 py-3">Type</th>
                <th className="px-4 py-3">Risk Score</th>
                <th className="px-4 py-3">Reputation</th>
                <th className="px-4 py-3">Source</th>
                <th className="px-4 py-3">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-cyber-700">
              {iocs.map((ioc) => (
                <tr key={ioc.id} className="hover:bg-cyber-700/50">
                  <td className="px-4 py-3 font-mono text-cyan-200">{ioc.value}</td>
                  <td className="px-4 py-3">
                    <span className={`rounded-full px-2 py-1 text-xs font-semibold ${getTypeColor(ioc.ioc_type)}`}>{ioc.ioc_type.toUpperCase()}</span>
                  </td>
                  <td className="px-4 py-3 font-semibold text-orange-300">{ioc.risk_score.toFixed(1)}</td>
                  <td className="px-4 py-3">{(ioc.reputation * 100).toFixed(0)}%</td>
                  <td className="px-4 py-3 text-slate-400">{ioc.source || "—"}</td>
                  <td className="px-4 py-3">
                    <span className="rounded bg-emerald-900 px-2 py-1 text-xs text-emerald-300">{ioc.status}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default IOCCenter;
