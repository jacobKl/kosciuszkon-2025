import React, { useState, type SyntheticEvent, useRef } from "react";
import Card from "../Card";
import Input from "../Input";
import { useAppContext, type DetailedConfiguratorState } from "../../context/AppContextProvider";
import { useForm } from "react-hook-form";
import EstimatorModal from "../EstimatorModal";
import { useEstimateEnergy } from "../../mutations/useEstimateEnergy";

const DetailedForm = () => {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { setStep, detailedConfiguratorState, setDetailedConfiguratorState } = useAppContext();
  const [isModalOpen, setIsModalOpen] = useState(false);

  const {
    handleSubmit,
    formState: { errors },
    register,
  } = useForm();

  const onSubmit = (data: DetailedConfiguratorState) => {
    setDetailedConfiguratorState(data);
    setStep(4);
  };

  const openModal = (e: SyntheticEvent) => {
    e.preventDefault();
    setIsModalOpen(true);
  };

  const mutation = useEstimateEnergy();

  const onModalSubmit = async (data: any) => {
    mutation.mutate(data, {
      onSuccess: (result) => {
        const { predicted_kwh } = result;
        if (inputRef.current) {
          inputRef.current.value = predicted_kwh;
        }
        setIsModalOpen(false);
      },
      onError: (error) => {
        console.error("Estimation failed", error);
      },
    });
  };

  return (
    <>
      <Card full={true} title="Szczegółowe informacje">
        <form className="grid grid-cols-3 gap-6" onSubmit={handleSubmit(onSubmit)}>
          <Input name="panel_installation_cost" label="Koszt instalacji [PLN]" register={register("panel_installation_cost")} error={errors?.panel_installation_cost?.message} />

          <Input
            name="energy_price_buy_kwh"
            label="Cena zakupu 1kWh [PLN]"
            register={register("energy_price_buy_kwh")}
            defaultValue={detailedConfiguratorState?.energy_price_buy_kwh}
            error={errors?.energy_price_buy_kwh?.message}
          />

          <Input
            name="energy_price_sell_kwh"
            label="Cena sprzedaży 1kWh [PLN]"
            register={register("energy_price_sell_kwh")}
            defaultValue={detailedConfiguratorState?.energy_price_sell_kwh}
            error={errors?.energy_price_sell_kwh?.message}
          />

          <Input defaultValue={7} name="energy_price_growth" label="Wzrost ceny energii rok do roku [%]" register={register("energy_price_growth")} error={errors?.energy_price_growth?.message} />
          <div className="grid grid-cols-2 gap-4">
            <Input ref={inputRef} name="energy_per_year" label="Zużycie roczne [kWh]" register={register("energy_per_year")} error={errors?.energy_per_year?.message} />

            <div>
              <button onClick={openModal} className="button-primary">
                Estymuj
              </button>
            </div>
          </div>
          <Input name="hourly_production_kw" label="Produkcja na godzinę [kWh]" register={register("hourly_production_kw")} error={errors?.hourly_production_kw?.message} />

          <Input defaultValue={22} name="consumption_level" label="Poziom konsumpcji [%]" register={register("consumption_level")} error={errors?.consumption_level?.message} />

          <div className="col-span-3 flex justify-end">
            <input className="button-primary" type="submit" value="Dalej" />
          </div>
        </form>
      </Card>
      <EstimatorModal isModalOpen={isModalOpen} setIsModalOpen={setIsModalOpen} onModalSubmit={onModalSubmit} />
    </>
  );
};

export default DetailedForm;
