import { useMemo } from "react";

export function useAuth() {
  const token = useMemo(() => localStorage.getItem("netsentinel_token"), []);
  return {
    isAuthenticated: Boolean(token),
    token,
  };
}
