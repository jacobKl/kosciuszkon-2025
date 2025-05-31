import React from "react";
import { useForm } from "react-hook-form";

import Input from "../Input";
import { useAppContext, type AppContextType, type FormState } from "../../context/AppContextProvider";

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
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-6 min-w-[500px]">
          <Input
            label="Adres"
            register={register("address", {
              required: "To pole jest wymagane",
            })}
            error={errors?.address?.message}
            name="address"
            helper="Potrzebujemy twojego adresu, żeby uzyskać wymiary dachu."
          />

          <Input
            label="Kod pocztowy"
            register={register("postcode", {
              required: "To pole jest wymagane",
            })}
            error={errors?.postcode?.message}
            name="postcode"
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
  );
};

export default AddressForm;
