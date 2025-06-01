import { type Dispatch, type SetStateAction } from "react";
import { useForm } from "react-hook-form";

import Modal from "../Modal";
import Input from "../Input";
import Checkbox from "../Checkbox";

const EstimatorModal = ({ isModalOpen, setIsModalOpen, onModalSubmit }: { isModalOpen: boolean; setIsModalOpen: Dispatch<SetStateAction<boolean>>; onModalSubmit: any }) => {
  const {
    register,
    formState: { errors },
    handleSubmit,
  } = useForm();

  return (
    <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
      <h2 className="text-xl mb-6">Estymator zużycia energii</h2>

      <form onSubmit={handleSubmit(onModalSubmit)} className="flex flex-col gap-4">
        <Input
          label="Liczba łazienek"
          register={register("ncombath", {
            required: "To pole jest wymagane",
          })}
          error={errors?.ncombath?.message}
        />
        <Input
          label="Liczba pokoi"
          register={register("totrooms", {
            required: "To pole jest wymagane",
          })}
          error={errors?.totrooms?.message}
        />
        <Input
          label="Ilość mieszkańcow"
          register={register("nhsldmem", {
            required: "To pole jest wymagane",
          })}
          error={errors?.nhsldmem?.message}
        />
        <Input
          label="Liczba ludzi na stałe w domu"
          register={register("athome", {
            required: "To pole jest wymagane",
          })}
          error={errors?.athome?.message}
          helper="np. osoby starsze"
        />
        <Input
          label="Liczba urządzeń o dużym zużyciu energii"
          register={register("num_devices", {
            required: "To pole jest wymagane",
          })}
          error={errors?.num_devices?.message}
        />

        <Checkbox label="Wysoki sufit" register={register("highceil")} error={errors?.highceil?.message} />

        <Checkbox label="Klimatyzacja" register={register("aircond")} error={errors?.aircond?.message} />

        <div className="flex justify-end">
          <input className="button-primary" type="submit" value="Estymuj" />
        </div>
      </form>
    </Modal>
  );
};

export default EstimatorModal;
