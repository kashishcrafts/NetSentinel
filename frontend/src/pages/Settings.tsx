function Settings() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">Settings</h2>
        <p className="mt-2 text-slate-400">Configure platform and system settings.</p>
      </div>

      <div className="grid gap-6">
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-xl font-semibold text-cyan-100">General Settings</h3>
          <div className="mt-6 space-y-6">
            <div>
              <label className="text-sm text-slate-400">Platform Name</label>
              <input
                type="text"
                defaultValue="NetSentinel"
                className="mt-2 w-full max-w-md rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400"
              />
            </div>
            <div>
              <label className="text-sm text-slate-400">API Rate Limit (requests/min)</label>
              <input
                type="number"
                defaultValue="1000"
                className="mt-2 w-full max-w-md rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400"
              />
            </div>
            <div>
              <label className="text-sm text-slate-400">Session Timeout (minutes)</label>
              <input
                type="number"
                defaultValue="30"
                className="mt-2 w-full max-w-md rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400"
              />
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-xl font-semibold text-cyan-100">AI Model Settings</h3>
          <div className="mt-6 space-y-6">
            <div>
              <label className="text-sm text-slate-400">Active Model Version</label>
              <select className="mt-2 w-full max-w-md rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400">
                <option>v1.0.0 - Isolation Forest</option>
                <option>v1.1.0 - Ensemble (IF + RFC)</option>
                <option>v1.2.0 - Neural (LSTM)</option>
              </select>
            </div>
            <div>
              <label className="text-sm text-slate-400">Anomaly Threshold</label>
              <input
                type="range"
                min="0"
                max="100"
                defaultValue="70"
                className="mt-2 w-full max-w-md"
              />
              <p className="mt-1 text-xs text-slate-400">70%</p>
            </div>
          </div>
        </div>

        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-xl font-semibold text-cyan-100">Threat Intelligence Sources</h3>
          <div className="mt-6 space-y-3">
            {["VirusTotal", "AbuseIPDB", "AlienVault OTX", "MITRE ATT&CK"].map((source) => (
              <label key={source} className="flex items-center gap-3">
                <input type="checkbox" defaultChecked className="h-4 w-4" />
                <span className="text-white">{source}</span>
              </label>
            ))}
          </div>
        </div>

        <div className="flex gap-3">
          <button className="rounded-lg bg-cyan-600 px-6 py-2 font-semibold text-white hover:bg-cyan-500">Save Settings</button>
          <button className="rounded-lg border border-cyber-700 px-6 py-2 font-semibold text-slate-400 hover:text-white">Cancel</button>
        </div>
      </div>
    </div>
  );
}

export default Settings;
