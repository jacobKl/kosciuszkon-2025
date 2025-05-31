import React, { useState } from "react";
import Card from "../Card";
import Input from "../Input";
import { useAppContext } from "../../context/AppContextProvider";
import { useForm } from "react-hook-form";

const DetailedForm = () => {
  const { setStep, detailedConfiguratorState, setDetailedConfiguratorState } = useAppContext();

  const {
    handleSubmit,
    formState: { errors },
    register,
  } = useForm();

  const onSubmit = (data: DetailedConfigurationState) => {
    setDetailedConfiguratorState(data);
    setStep(4);
  };

  return (
    <Card full={true}>
      <form className="grid grid-cols-3 gap-4" onSubmit={handleSubmit(onSubmit)}>
        <Input
          name="panel_installation_cost"
          label="Koszt instalacji panelu"
          register={register("panel_installation_cost")}
          error={errors?.panel_installation_cost?.message}
        />
        <Input
          name="energy_price_buy_kwh"
          label="Cena zakupu 1kWh"
          register={register("energy_price_buy_kwh")}
          defaultValue={detailedConfiguratorState?.energy_price_buy_kwh}
          error={errors?.energy_price_buy_kwh?.message}
        />

        <Input
          name="energy_price_sell_kwh"
          label="Cena sprzedaży 1kWh"
          register={register("energy_price_sell_kwh")}
          defaultValue={detailedConfiguratorState?.energy_price_sell_kwh}
          error={errors?.energy_price_sell_kwh?.message}
        />

        <Input
          name="energy_price_growth"
          label="Wzrost ceny energii rok do roku"
          register={register("energy_price_growth")}
          error={errors?.energy_price_growth?.message}
        />
        <Input
          name="energy_per_year"
          label="Zużycie roczne"
          register={register("energy_per_year")}
          error={errors?.energy_per_year?.message}
        />
        <Input
          name="hourly_production_kw"
          label="Produkcja kWh na godzinę"
          register={register("hourly_production_kw")}
          error={errors?.hourly_production_kw?.message}
        />

        <Input
          name="consumption_level"
          label="Poziom konsumpcji"
          register={register("consumption_level")}
          error={errors?.consumption_level?.message}
        />

        <div className="col-span-3 flex justify-end">
          <input className="button-primary" type="submit" value="Dalej" />
        </div>
      </form>
    </Card>
  );
};

export default DetailedForm;
