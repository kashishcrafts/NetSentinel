import { useEffect, useState } from "react";
import api from "../services/api";
import AlertTable from "../components/AlertTable";

function Alerts() {
  const [alerts, setAlerts] = useState<any[]>([]);

  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await api.get("/alerts");
        setAlerts(response.data || []);
      } catch (error) {
        console.error(error);
      }
    };

    fetchAlerts();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Alerts</h2>
        <p className="mt-2 text-slate-400">View all security alerts and current status.</p>
      </div>
      <AlertTable alerts={alerts} />
    </div>
  );
}

export default Alerts;
