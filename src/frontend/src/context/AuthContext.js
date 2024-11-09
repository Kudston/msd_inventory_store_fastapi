import React, { createContext, useState, useContext } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const [user, setUser] = useState(null);

  const login = (token, userData) => {
    setAccessToken(token);
    setUser(userData);
  };

  const logout = () => {
    setAccessToken(null);
    setUser({
      "user_name":"No User",
      "is_admin":false
    });
  };

  return (
    <AuthContext.Provider value={{ accessToken, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);