import { useState, type SyntheticEvent, useRef } from "react";
import Card from "../Card";
import Input from "../Input";
import {
  useAppContext,
  type DetailedConfiguratorState,
} from "../../context/AppContextProvider";
import { useForm } from "react-hook-form";
import EstimatorModal from "../EstimatorModal";
import { useEstimateEnergy } from "../../mutations/useEstimateEnergy";
import { useAddressQuery } from "../../queries/useAddressQuery";

const DetailedForm = () => {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { setStep, detailedConfiguratorState, setDetailedConfiguratorState } =
    useAppContext();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const roofConfiguration = JSON.parse(
    localStorage.getItem("roofConfigurator")!,
  );
  console.warn(roofConfiguration);

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

  const { formState } = useAppContext();
  const { data } = useAddressQuery(formState);

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
        <form
          className="grid grid-cols-3 gap-6"
          onSubmit={handleSubmit(onSubmit)}
        >
          <Input
            defaultValue={
              parseInt(roofConfiguration.solar_amount) * 0.35 * 5000
            }
            unit="PLN"
            name="panel_installation_cost"
            label="Koszt instalacji"
            register={register("panel_installation_cost")}
            error={errors?.panel_installation_cost?.message}
          />

          <Input
            unit="PLN"
            name="energy_price_buy_kwh"
            label="Cena zakupu 1kWh"
            register={register("energy_price_buy_kwh")}
            defaultValue={detailedConfiguratorState?.energy_price_buy_kwh}
            error={errors?.energy_price_buy_kwh?.message}
          />

          <Input
            unit="PLN"
            name="energy_price_sell_kwh"
            label="Cena sprzedaży 1kWh"
            register={register("energy_price_sell_kwh")}
            defaultValue={detailedConfiguratorState?.energy_price_sell_kwh}
            error={errors?.energy_price_sell_kwh?.message}
          />

          <Input
            unit="%"
            defaultValue={7}
            name="energy_price_growth"
            label="Wzrost ceny energii rok do roku"
            register={register("energy_price_growth")}
            error={errors?.energy_price_growth?.message}
          />
          <div className="flex items-center">
            <Input
              unit="kWh"
              ref={inputRef}
              name="energy_per_year"
              label="Zużycie roczne"
              register={register("energy_per_year")}
              error={errors?.energy_per_year?.message}
            />

            <div className="pl-2">
              <button onClick={openModal} className="p-1 bg-gray-100 rounded">
                Estymuj
              </button>
            </div>
          </div>
          <Input
            defaultValue={
              (data?.features[0]?.properties?.solar_panels?.flat?.solar_output
                ?.clear?.estimated_production_per_hour /
                1000) *
              parseInt(roofConfiguration.solar_amount)
            }
            unit="kWh"
            name="hourly_production_kw"
            label="Produkcja na godzinę"
            register={register("hourly_production_kw")}
            error={errors?.hourly_production_kw?.message}
          />

          <Input
            unit="%"
            defaultValue={22}
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
      <EstimatorModal
        isModalOpen={isModalOpen}
        setIsModalOpen={setIsModalOpen}
        onModalSubmit={onModalSubmit}
      />
    </>
  );
};

export default DetailedForm;
