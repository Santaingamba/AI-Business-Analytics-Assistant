import { createContext, useContext, useState, ReactNode } from 'react';

export interface DashboardFilters {
  dateRange: [Date | null, Date | null];
  category: string | null;
  region: string | null;
  customerSegment: string | null;
}

interface DashboardContextState {
  filters: DashboardFilters;
  setFilters: (filters: Partial<DashboardFilters>) => void;
  resetFilters: () => void;
  activeDatasetId: string | null;
  setActiveDatasetId: (id: string | null) => void;
}

const defaultFilters: DashboardFilters = {
  dateRange: [null, null],
  category: null,
  region: null,
  customerSegment: null,
};

const DashboardContext = createContext<DashboardContextState | undefined>(undefined);

export function DashboardProvider({ children }: { children: ReactNode }) {
  const [filters, setFiltersState] = useState<DashboardFilters>(defaultFilters);
  const [activeDatasetId, setActiveDatasetId] = useState<string | null>(null);

  const setFilters = (newFilters: Partial<DashboardFilters>) => {
    setFiltersState((prev) => ({ ...prev, ...newFilters }));
  };

  const resetFilters = () => {
    setFiltersState(defaultFilters);
  };

  return (
    <DashboardContext.Provider
      value={{
        filters,
        setFilters,
        resetFilters,
        activeDatasetId,
        setActiveDatasetId,
      }}
    >
      {children}
    </DashboardContext.Provider>
  );
}

export function useDashboard() {
  const context = useContext(DashboardContext);
  if (context === undefined) {
    throw new Error('useDashboard must be used within a DashboardProvider');
  }
  return context;
}
