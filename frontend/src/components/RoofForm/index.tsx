import React, { useState } from "react";
import Card from "../Card";
import HomeScene from "../HomeScene";
import ControlledInput from "../ControlledInput";
import { useAppContext } from "../../context/AppContextProvider";
import Select from "../Select";

type RoofConfigurator = {
  roof_height: number;
  building_height: number;
  roof_angle: number;
  roof_orientation: boolean;
  roof_type: "flat" | "gable";
};

const orientationOptions = [
  { value: 1, label: "Orientacja 1" },
  { value: 0, label: "Orientacja 2" },
];

const roofOptions = [
  { value: "flat", label: "Płaski" },
  { value: "gable", label: "Dwuspadowy" },
];

const RoofForm = () => {
  const { step, setStep } = useAppContext();

  const [roofConfiguratorState, setRoofConfiguratorState] = useState<RoofConfigurator>({
    roof_height: 3,
    building_height: 10,
    roof_angle: 30,
    roof_orientation: false,
    roof_type: "flat",
  });

  const updateConfiguration = (name: string, value: any) => {
    setRoofConfiguratorState({
      ...roofConfiguratorState,
      [name]: value,
    });
  };

  return (
    <Card title="Szczegółowa konfiguracja" full={true} innerPadding={false}>
      <div className="grid grid-cols-3">
        <div className="col-span-2">
          <HomeScene />
        </div>
        <div className="col-span-1 flex flex-col justify-between items-stretch">
          <div className="py-3">
            <div className="flex flex-col gap-4 px-4 py-2">
              <ControlledInput onInput={(e) => updateConfiguration("roof_height", e.target.value)} label={"Wysokość dachu [m]"} value={roofConfiguratorState.roof_height} />

              <ControlledInput onInput={(e) => updateConfiguration("building_height", e.target.value)} label={"Wysokość budynku [m]"} value={roofConfiguratorState.building_height} />

              <ControlledInput onInput={(e) => updateConfiguration("roof_angle", e.target.value)} label={"Kąt dachu"} value={roofConfiguratorState.roof_angle} />

              <Select value={roofConfiguratorState.roof_orientation} onChange={(value: string) => updateConfiguration("roof_orientation", value)} options={orientationOptions} />

              <Select value={roofConfiguratorState.roof_type} onChange={(value: string) => updateConfiguration("roof_type", value)} options={roofOptions} />

              <div className="mt-10 flex justify-end">
                <button className="button-primary" onClick={() => setStep(step + 1)}>
                  Dalej
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default RoofForm;
