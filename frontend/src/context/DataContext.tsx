"use client";

import { createContext, useContext, useState, ReactNode } from "react";
import { ScraperResponse } from "@/app/results/page";

interface DataContextType {
  data: ScraperResponse;
  setData: React.Dispatch<React.SetStateAction<any | null>>;
}

interface DataProviderProps {
  children: ReactNode;
}

const DataContext = createContext<DataContextType | undefined>(undefined);

export const DataProvider: React.FC<DataProviderProps> = ({ children }) => {
  const [data, setData] = useState(null);

  return (
    <DataContext.Provider value={{ data, setData }}>
      {children}
    </DataContext.Provider>
  );
};

export function useData(): DataContextType {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error("useData must be used within a DataProvider");
  }
  return context;
}
