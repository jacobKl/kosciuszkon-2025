import clsx from "clsx";
import React from "react";
import CountUp from "../CountUp";

type InfoCardProps = {
  value: string;
  text: string;
  unit?: string;
  icon?: React.ReactNode;
  className?: string;
  animate?: boolean;
};

const InfoCard: React.FC<InfoCardProps> = ({
  value,
  icon,
  text,
  unit,
  className = "",
  animate = false,
}) => {
  return (
    <div
      className={clsx(
        "p-6 rounded-2xl shadow-sm border bg-white flex flex-col justify-between",
        className
      )}
    >
      <div className="flex items-center gap-3 mb-4">
        {icon && (
          <div className="w-9 h-9 flex items-center justify-center rounded-full bg-gray-100 text-gray-600">
            {icon}
          </div>
        )}
        <span className="text-gray-800 text-base font-medium">{text}</span>
      </div>

      <div className="text-3xl font-bold text-gray-900">
        {animate ? <CountUp to={value} /> : <span>{value}</span>}
        {unit && <span className="ml-1 text-gray-700 text-2xl">{unit}</span>}
      </div>
    </div>
  );
};

export default InfoCard;
