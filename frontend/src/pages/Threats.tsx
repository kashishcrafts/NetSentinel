import { useEffect, useState } from "react";
import api from "../services/api";
import ThreatTable from "../components/ThreatTable";

function Threats() {
  const [threats, setThreats] = useState<any[]>([]);

  useEffect(() => {
    const fetchThreats = async () => {
      try {
        const response = await api.get("/threats");
        setThreats(response.data || []);
      } catch (error) {
        console.error(error);
      }
    };

    fetchThreats();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Threat Intelligence</h2>
        <p className="mt-2 text-slate-400">Monitor detected threats across your network.</p>
      </div>
      <ThreatTable threats={threats} />
    </div>
  );
}

export default Threats;
