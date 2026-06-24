import { useEffect, useState } from "react";
import { BarChart, Bar, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, PieChart, Pie, Legend } from "recharts";
import api from "../services/api";

function Analytics() {
  const [severityData, setSeverityData] = useState<any[]>([]);
  const [alertData, setAlertData] = useState<any[]>([]);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        const threatsResponse = await api.get("/threats");
        const alertsResponse = await api.get("/alerts");

        const threats = threatsResponse.data || [];
        const alerts = alertsResponse.data || [];

        const severityCounts = threats.reduce((acc: any, threat: any) => {
          const key = threat.severity || "unknown";
          acc[key] = (acc[key] || 0) + 1;
          return acc;
        }, {});

        setSeverityData(
          Object.entries(severityCounts).map(([severity, count]) => ({
            name: severity,
            value: count
          }))
        );

        const statusCounts = alerts.reduce((acc: any, alert: any) => {
          const key = alert.status || "unknown";
          acc[key] = (acc[key] || 0) + 1;
          return acc;
        }, {});

        setAlertData(
          Object.entries(statusCounts).map(([status, count]) => ({
            name: status,
            count
          }))
        );
      } catch (error) {
        console.error(error);
      }
    };

    fetchAnalytics();
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Analytics</h2>
        <p className="mt-2 text-slate-400">Actionable security metrics from your NetSentinel deployment.</p>
      </div>
      <div className="grid gap-6 xl:grid-cols-2">
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-xl font-semibold text-cyan-100">Threat Severity Distribution</h3>
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={severityData} dataKey="value" nameKey="name" innerRadius={60} outerRadius={100} paddingAngle={3}>
                  {severityData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={["#22d3ee", "#38bdf8", "#f97316", "#ef4444"][index % 4]} />
                  ))}
                </Pie>
                <Legend verticalAlign="bottom" height={36} />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: 14, border: "1px solid #334155" }} itemStyle={{ color: "#f8fafc" }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <h3 className="text-xl font-semibold text-cyan-100">Alert Overview</h3>
          <div className="mt-6 h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={alertData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="name" stroke="#94a3b8" />
                <YAxis stroke="#94a3b8" />
                <Tooltip contentStyle={{ backgroundColor: "#0f172a", borderRadius: 14, border: "1px solid #334155" }} itemStyle={{ color: "#f8fafc" }} />
                <Bar dataKey="count" fill="#38bdf8">
                  {alertData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={["#38bdf8", "#0ea5e9", "#8b5cf6", "#f43f5e"][index % 4]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Analytics;
