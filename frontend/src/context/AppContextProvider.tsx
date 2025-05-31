import React, { useState, type ReactNode, createContext, type Dispatch, type SetStateAction, useContext } from "react";

export type FormState = {
  street: string;
  number: string;
  postcode: string;
  city: string;
};

export type AppContextType = {
  step: number;
  setStep: Dispatch<SetStateAction<number>>;

  formState: FormState;
  setFormState: Dispatch<SetStateAction<FormState>>;
};

const AppContext = createContext<AppContextType | undefined>(undefined);

const AppContextProvider = ({ children }: { children: ReactNode }) => {
  const [step, setStep] = useState(1);
  const [formState, setFormState] = useState<FormState>({
    street: "",
    number: "",
    postcode: "",
    city: "",
  });

  return (
    <AppContext.Provider value={{ formState, setFormState, step, setStep }}>
      {children}
    </AppContext.Provider>
  );
};

const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error("useAppContext must be used within a FormContextProvider");
  }
  return context;
};

export { AppContextProvider, useAppContext };