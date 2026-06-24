import { useEffect, useState } from "react";
import api from "../services/api";

const ROLES = [
  { value: "super_admin", label: "Super Admin", color: "red" },
  { value: "admin", label: "Admin", color: "orange" },
  { value: "soc_analyst", label: "SOC Analyst", color: "blue" },
  { value: "threat_hunter", label: "Threat Hunter", color: "purple" },
  { value: "incident_responder", label: "Incident Responder", color: "pink" },
  { value: "viewer", label: "Viewer", color: "gray" },
];

function UserManagement() {
  const [users, setUsers] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [showNewUser, setShowNewUser] = useState(false);

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await api.get("/api/v1/users");
      setUsers(response.data.data || []);
    } catch (error) {
      console.error(error);
    }
  };

  const getRoleColor = (role: string) => {
    const roleObj = ROLES.find((r) => r.value === role);
    const colors: any = {
      red: "bg-red-900 text-red-300",
      orange: "bg-orange-900 text-orange-300",
      blue: "bg-blue-900 text-blue-300",
      purple: "bg-purple-900 text-purple-300",
      pink: "bg-pink-900 text-pink-300",
      gray: "bg-gray-900 text-gray-300",
    };
    return colors[roleObj?.color || "gray"];
  };

  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-3xl font-semibold text-cyan-200">User Management</h2>
        <p className="mt-2 text-slate-400">Manage users and their permissions.</p>
      </div>

      <button onClick={() => setShowNewUser(!showNewUser)} className="rounded-full bg-cyan-600 px-6 py-2 font-semibold text-white hover:bg-cyan-500">
        + Add User
      </button>

      {showNewUser && (
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
          <h3 className="text-lg font-semibold text-cyan-100">New User</h3>
          <div className="mt-4 space-y-4">
            <div>
              <label className="text-sm text-slate-400">Email</label>
              <input type="email" className="mt-1 w-full rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400" />
            </div>
            <div>
              <label className="text-sm text-slate-400">Role</label>
              <select className="mt-1 w-full rounded-lg border border-cyber-700 bg-cyber-700 px-4 py-2 text-white outline-none focus:border-cyan-400">
                {ROLES.map((role) => (
                  <option key={role.value} value={role.value}>
                    {role.label}
                  </option>
                ))}
              </select>
            </div>
            <button className="w-full rounded-lg bg-cyan-600 px-4 py-2 font-semibold text-white hover:bg-cyan-500">Create User</button>
          </div>
        </div>
      )}

      <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6">
        <h3 className="text-lg font-semibold text-cyan-100">Users ({users.length})</h3>
        <div className="mt-4 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {users.map((user) => (
            <div key={user.id} onClick={() => setSelectedUser(user)} className="cursor-pointer rounded-lg border border-cyber-700 bg-cyber-700/50 p-4 transition hover:border-cyan-400">
              <div className="flex items-start justify-between">
                <div>
                  <p className="font-semibold text-white">{user.email}</p>
                  <p className="mt-1 text-sm text-slate-400">{user.full_name || "No name"}</p>
                </div>
              </div>
              <div className="mt-3 flex gap-2">
                <span className={`rounded-full px-2 py-1 text-xs font-semibold ${getRoleColor(user.role)}`}>{ROLES.find((r) => r.value === user.role)?.label}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {selectedUser && (
        <div className="rounded-3xl border border-cyber-700 bg-cyber-800 p-6 shadow-glow">
          <div className="flex justify-between items-start">
            <div>
              <h3 className="text-lg font-semibold text-cyan-100">{selectedUser.email}</h3>
              <p className="mt-1 text-slate-400">{selectedUser.full_name}</p>
            </div>
            <button onClick={() => setSelectedUser(null)} className="text-slate-400 hover:text-white">
              ✕
            </button>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div>
              <p className="text-sm text-slate-400">Role</p>
              <p className="mt-1 text-lg font-semibold text-cyan-200">{ROLES.find((r) => r.value === selectedUser.role)?.label}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Status</p>
              <p className="mt-1 text-lg font-semibold text-emerald-300">Active</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Created</p>
              <p className="mt-1 text-sm text-slate-300">{new Date(selectedUser.created_at).toLocaleDateString()}</p>
            </div>
            <div>
              <p className="text-sm text-slate-400">Last Login</p>
              <p className="mt-1 text-sm text-slate-300">{selectedUser.last_login ? new Date(selectedUser.last_login).toLocaleDateString() : "Never"}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default UserManagement;
