import React from "react";

import type { UseFormRegisterReturn } from "react-hook-form";

type InputProps = {
  label: string;
  register: UseFormRegisterReturn;
  name: string;
  helper?: string;
  error?: string | undefined | null;
  defaultValue?: string | number;
  unit?: string;
};

const Input = React.forwardRef<HTMLInputElement, InputProps>(({ label, register, name, helper, error, defaultValue, unit }, ref) => {
  return (
    <div className="flex flex-col relative w-full">
      <input
        defaultValue={defaultValue}
        {...register}
        ref={(el) => {
          register.ref(el);
          if (typeof ref === "function") ref(el);
          else if (ref) (ref as React.MutableRefObject<HTMLInputElement | null>).current = el;
        }}
        type="text"
        id={name}
        className="peer h-12 w-full border-b-[1px] border-gray-200 text-gray-900 placeholder-transparent focus:outline-none focus:border-primary"
        placeholder="Your name"
      />
      {unit && <span className="absolute right-1 bottom-3 text-gray-400 font-thin">{unit}</span>}
      <label
        htmlFor={name}
        className="absolute pointer-events-none font-thin left-0 -top-2 text-gray-600 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-3 peer-focus:-top-2 peer-focus:text-gray-600 peer-focus:text-sm"
      >
        {label}
      </label>
      {error && <p className="text-red-500 mt-3 font-thin text-sm">{error}</p>}
      {helper && <p className="text-gray-500 mt-3 font-thin text-sm">{helper}</p>}
    </div>
  );
});

Input.displayName = "Input";

export default Input;
