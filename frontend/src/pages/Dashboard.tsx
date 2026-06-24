import { useEffect, useState } from "react";
import api from "../services/api";
import DashboardCard from "../components/DashboardCard";

function Dashboard() {
  const [totalThreats, setTotalThreats] = useState(0);
  const [openAlerts, setOpenAlerts] = useState(0);
  const [reportsGenerated, setReportsGenerated] = useState(0);
  const [criticalThreats, setCriticalThreats] = useState(0);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const threatsResponse = await api.get("/threats");
        const alertsResponse = await api.get("/alerts");
        const reportsResponse = await api.get("/reports");

        const threats = threatsResponse.data || [];
        const alerts = alertsResponse.data || [];
        const reports = reportsResponse.data || [];

        setTotalThreats(threats.length);
        setOpenAlerts(alerts.filter((alert: any) => alert.status === "open").length);
        setReportsGenerated(reports.length);
        setCriticalThreats(threats.filter((threat: any) => threat.severity.toLowerCase() === "critical").length);
      } catch (error) {
        console.error(error);
      }
    };

    fetchStats();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Dashboard</h2>
        <p className="mt-2 text-slate-400">Live overview of threats, alerts, and reports.</p>
      </div>
      <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-4">
        <DashboardCard label="Total Threats" value={totalThreats} icon="🛡️" accent="bg-cyan-300" />
        <DashboardCard label="Open Alerts" value={openAlerts} icon="🚨" accent="bg-rose-300" />
        <DashboardCard label="Reports Generated" value={reportsGenerated} icon="📊" accent="bg-emerald-300" />
        <DashboardCard label="Critical Threats" value={criticalThreats} icon="🔥" accent="bg-orange-300" />
      </div>
    </div>
  );
}

export default Dashboard;
