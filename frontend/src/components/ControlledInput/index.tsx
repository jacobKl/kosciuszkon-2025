import React from "react";

const ControlledInput = ({ label, value, onInput, name, helper, error }: { label: string; value: any; onInput: any; name: string; helper?: string; error: any; }) => {
  return (
    <div className="flex flex-col relative w-full">
      <input value={value} onInput={onInput} type="text" id={name} className="peer h-12 w-full border-b-[1px] border-gray-200 text-gray-900 placeholder-transparent focus:outline-none focus:border-primary" placeholder="Your name" />
      <label
        htmlFor={name}
        className="absolute pointer-events-none font-thin left-0 -top-3.5 text-gray-600 text-sm transition-all peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-400 peer-placeholder-shown:top-3 peer-focus:-top-3.5 peer-focus:text-gray-600 peer-focus:text-sm"
      >
        {label}
      </label>
      {error && <p className="text-red-500 mt-3 font-thin text-sm">{error}</p>}
      <p className="text-gray-500 mt-3 font-thin text-sm">{helper}</p>
    </div>
  );
};

export default ControlledInput;
