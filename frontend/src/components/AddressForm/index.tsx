import React from "react";
import { useForm } from "react-hook-form";

import { useAppContext, type AppContextType, type FormState } from "../../context/AppContextProvider";

import Input from "../Input";
import Card from "../Card";

const AddressForm = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm({});

  const { setStep, setFormState } : AppContextType = useAppContext();

  const onSubmit = (data : FormState) => {
    setFormState(data);
    setStep(2);
  }

  return (
      <Card title="Dane teleadresowe">
        <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6 min-w-[500px]">
          <Input
            label="Ulica"
            register={register("street", {
              required: "To pole jest wymagane",
            })}
            error={errors?.street?.message}
            name="street"
            helper="Potrzebujemy twojego adresu, żeby uzyskać wymiary dachu."
          />

          <Input
            label="Numer domu"
            register={register("number", {
              required: "To pole jest wymagane",
            })}
            error={errors?.number?.message}
            name="number"
          />

          <Input
            label="Kod pocztowy"
            register={register("postalcode", {
              required: "To pole jest wymagane",
            })}
            error={errors?.postalcode?.message}
            name="postalcode"
          />

          <Input
            label="Miejscowość"
            register={register("city", {
              required: "To pole jest wymagane",
            })}
            error={errors?.city?.message}
            name="city"
          />

        <div className="flex justify-end">
          <input type="submit" value="Dalej" className="button-primary" />
        </div>
      </form>
      </Card>
  );
};

export default AddressForm;
