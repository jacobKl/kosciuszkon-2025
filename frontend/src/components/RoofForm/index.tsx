import React, { useState } from "react";
import Card from "../Card";
import HomeScene from "../HomeScene";
import ControlledInput from "../ControlledInput";
import clsx from "clsx";
import { useAppContext } from "../../context/AppContextProvider";

type RoofConfigurator = {
  roof_height: number;
  building_height: number;
  roof_angle: number;
  roof_orientation: boolean;
  roof_type: "flat" | "gable";
};

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
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-2">
          <HomeScene />
        </div>
        <div className="col-span-1 flex flex-col justify-between items-stretch">
          <div className="py-3">
            <div className="flex flex-col gap-2">
              <ControlledInput onInput={(e) => updateConfiguration("roof_height", e.target.value)} label={"Wysokość dachu [m]"} value={roofConfiguratorState.roof_height} />

              <ControlledInput onInput={(e) => updateConfiguration("building_height", e.target.value)} label={"Wysokość budynku [m]"} value={roofConfiguratorState.building_height} />

              <ControlledInput onInput={(e) => updateConfiguration("roof_angle", e.target.value)} label={"Kąt dachu"} value={roofConfiguratorState.roof_angle} />

              <div>
                <h2 className="mb-4">Orientacja dachu:</h2>
                <div className="flex gap-4">
                  <button onClick={() => updateConfiguration("roof_orientation", false)} className={clsx("button-outline", !roofConfiguratorState.roof_orientation ? "bg-gray-400" : "bg-gray-300")}>
                    1
                  </button>

                  <button onClick={() => updateConfiguration("roof_orientation", true)} className={clsx("button-outline", roofConfiguratorState.roof_orientation ? "bg-gray-400" : "bg-gray-300")}>
                    2
                  </button>
                </div>
              </div>

              <div>
                <h2 className="mb-4">Typ dachu:</h2>
                <div className="flex gap-4">
                  <button onClick={() => updateConfiguration("roof_type", "flat")} className={clsx("button-outline", roofConfiguratorState.roof_type === "flat" ? "bg-gray-400" : "bg-gray-300")}>
                    Płaski
                  </button>

                  <button onClick={() => updateConfiguration("roof_type", "gable")} className={clsx("button-outline", roofConfiguratorState.roof_type === "gable" ? "bg-gray-400" : "bg-gray-300")}>
                    Dwuspadowy
                  </button>
                </div>
              </div>
            </div>

            <div className="mt-10 flex justify-between">
              <button className="button-primary" onClick={() => setStep(step + 1)}>
                Dalej
              </button>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default RoofForm;
