import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    if (localStorage.getItem("netsentinel_token")) {
      navigate("/");
    }
  }, [navigate]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError("");

    try {
      const response = await api.post("/users/login", { email, password });
      localStorage.setItem("netsentinel_token", response.data.access_token);
      navigate("/");
    } catch (e) {
      setError("Unable to authenticate. Check credentials and try again.");
    }
  };

  return (
    <div className="mx-auto flex min-h-[calc(100vh-64px)] max-w-2xl items-center justify-center px-4 py-10">
      <div className="w-full rounded-3xl border border-cyber-700 bg-cyber-900/95 p-10 shadow-glow">
        <h2 className="text-3xl font-semibold text-cyan-200">Secure Login</h2>
        <p className="mt-2 text-sm text-slate-400">Sign in to access NetSentinel intelligence.</p>
        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div>
            <label className="text-sm text-slate-300" htmlFor="email">Email</label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="mt-2 w-full rounded-3xl border border-cyber-700 bg-cyber-800 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-400"
              required
            />
          </div>
          <div>
            <label className="text-sm text-slate-300" htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="mt-2 w-full rounded-3xl border border-cyber-700 bg-cyber-800 px-4 py-3 text-sm text-slate-100 outline-none transition focus:border-cyan-400"
              required
            />
          </div>
          {error && <p className="text-sm text-rose-400">{error}</p>}
          <button className="w-full rounded-full bg-cyber-500 px-5 py-3 text-sm font-semibold text-slate-900 transition hover:bg-cyan-400">
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default Login;
