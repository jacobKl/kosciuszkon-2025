import React, { useState, type ReactNode, createContext, type Dispatch, type SetStateAction, useContext } from "react";

export type FormState = {
  street: string;
  number: string;
  postalcode: string;
  city: string;
  external_garage_count: string;
};

export type DetailedConfiguratorState = {
  panel_installation_cost: number | "";
  energy_price_buy_kwh: number | "";
  energy_price_sell_kwh: number | "";
  energy_price_growth: number | "";
  energy_per_year: number | "";
  hourly_production_kw: number | "";
  consumption_level: number | "";
};

export type AppContextType = {
  step: number;
  setStep: Dispatch<SetStateAction<number>>;

  formState: FormState;
  setFormState: Dispatch<SetStateAction<FormState>>;

  detailedConfiguratorState: DetailedConfiguratorState;
  setDetailedConfiguratorState: Dispatch<SetStateAction<DetailedConfiguratorState>>;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const AppContextProvider = ({ children }: { children: ReactNode }) => {
  const [step, setStep] = useState(3);
  const [formState, setFormState] = useState<FormState>({
    street: "",
    number: "",
    postalcode: "",
    city: "",
    external_garage_count: "",
  });

  const [detailedConfiguratorState, setDetailedConfiguratorState] = useState<DetailedConfiguratorState>({
    panel_installation_cost: "",
    energy_price_buy_kwh: 1.23,
    energy_price_sell_kwh: 0.51,

    energy_price_growth: "",
    energy_per_year: "",
    hourly_production_kw: "",
    consumption_level: "",
  });

  return <AppContext.Provider value={{ formState, setFormState, step, setStep, detailedConfiguratorState, setDetailedConfiguratorState }}>{children}</AppContext.Provider>;
};

const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within a FormContextProvider");
  }
  return context;
};

export { AppContextProvider, useAppContext };
