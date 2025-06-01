import React from "react";
import type { UseFormRegisterReturn } from "react-hook-form";

type CheckboxProps = {
  label: string;
  name: string;
  register: UseFormRegisterReturn;
  error?: string | null | undefined;
  labelYes?: string;
  labelNo?: string;
};

const Checkbox = ({ label, name, register, error, labelYes = "Tak", labelNo = "Nie" }: CheckboxProps) => {
  return (
    <div className="flex flex-col relative w-full">
      <div className="h-12 w-full border-b-[1px] border-gray-200 text-gray-900 placeholder-transparent focus-within:border-primary flex items-center gap-6">
        <label
          htmlFor={`${name}-yes`}
          className="pointer-events-none font-thin left-0 -top-2 text-gray-600 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-3 peer-focus:-top-2 peer-focus:text-gray-600 peer-focus:text-sm"
        >
          {label}
        </label>

        <label className="inline-flex items-center cursor-pointer">
          <input {...register} type="radio" id={`${name}-yes`} value={1} className="mr-2 h-5 w-5 border border-gray-300 text-primary focus:ring-primary" />
          <span>{labelYes}</span>
        </label>

        <label className="inline-flex items-center cursor-pointer">
          <input {...register} type="radio" id={`${name}-no`} value={0} className="mr-2 h-5 w-5 border border-gray-300 text-primary focus:ring-primary" />
          <span>{labelNo}</span>
        </label>
      </div>

      {error && <p className="text-red-500 mt-3 font-thin text-sm">{error}</p>}
    </div>
  );
};

export default Checkbox;
