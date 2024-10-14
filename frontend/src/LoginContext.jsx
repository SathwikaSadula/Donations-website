import React, { createContext, useContext, useState } from 'react';

const LoginContext = createContext();
export const useLogin = () => useContext(LoginContext);

export const LoginProvider = ({ children }) => {
  const [user,setUser]=useState({
    "partyId":"",
    "partyType":""
  });

  return (
    <LoginContext.Provider value={{user,setUser}}>
      {children}
    </LoginContext.Provider>
  );
};