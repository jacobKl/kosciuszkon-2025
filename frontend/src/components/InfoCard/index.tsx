import clsx from "clsx";
import React from "react";

import CountUp from "../CountUp";

const InfoCard = ({ value, icon, className, text, unit, animate = false }: { value: string; icon?: any; className: string; text: string; unit?: string; animate?: boolean }) => {
  return (
    <div className={clsx("p-6 rounded shadow", className)}>
      <div className="flex items-center gap-4 mb-6">
        {icon && <div>{icon}</div>}
        {text}
      </div>

      <div className="text-2xl font-bold">
        {animate ? <CountUp to={value} /> : <span>{value}</span>}
        <span>{unit}</span>
      </div>
    </div>
  );
};

export default InfoCard;
