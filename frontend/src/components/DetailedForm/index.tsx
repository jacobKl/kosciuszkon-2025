import React, { useState } from "react";
import Card from "../Card";
import HomeScene from "../HomeScene";
import ControlledInput from "../ControlledInput";

type DetailedConfigurationState = {
  panel_installation_cost: number | null;
  energy_price_buy_kwh: number | null;
  energy_price_sell_kwh: number | null;
  energy_price_growth: number | null;
  energy_per_year: number | null;
  hourly_production_kw: number | null;
  consumption_level: number | null;
};

const DetailedForm = () => {
  const [detailedConfigurationState, setDetailedConfigurationState] = useState<DetailedConfigurationState>({
    panel_installation_cost: null,
    energy_price_buy_kwh: null,
    energy_price_sell_kwh: null,
    energy_price_growth: null,
    energy_per_year: null,
    hourly_production_kw: null,
    consumption_level: null,
  });

  const updateConfiguration = (name: string, value: any) => {
    setDetailedConfigurationState({
      ...detailedConfigurationState,
      [name]: value,
    });
  };

  return (
    <Card title="Szczegółowa konfiguracja" full={true}>
      <div className="grid grid-cols-3">
        <div className="col-span-2">
          <HomeScene />
        </div>
        <div className="col-span-1 flex flex-col justify-between items-stretch">
          <div className="flex flex-col gap-1">
            <ControlledInput
              onInput={(e) => updateConfiguration("panel_installation_cost", e.target.value)}
              label={"Koszt instalacji panelu"}
              value={detailedConfigurationState.panel_installation_cost}
            />
            <ControlledInput label={"Cena zakupu 1kWh"} value={detailedConfigurationState.energy_price_buy_kwh} />
            <ControlledInput label={"Cena sprzedaży 1kWh"} value={detailedConfigurationState.energy_price_sell_kwh} />
            <ControlledInput label={"Wzrost ceny energii rok do roku"} value={detailedConfigurationState.energy_price_growth} />
            <ControlledInput label={"Dzienna produkcja kWh"} value={detailedConfigurationState.hourly_production_kw} />
            <ControlledInput label={"Konsumpcja"} value={detailedConfigurationState.consumption_level} />
          </div>

          <div className="mt-10 flex justify-between">
            <button className="button-secondary" onClick={() => setStep(step - 1)}>
              Cofnij
            </button>
            <button className="button-primary" onClick={() => setStep(step + 1)}>
              Dalej
            </button>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default DetailedForm;
