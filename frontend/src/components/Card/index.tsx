import clsx from "clsx";
import React, { type ReactNode } from "react";

const Card = ({ children, title, full = false, innerPadding = true }: { children: ReactNode; title?: string; full: boolean; innerPadding?: boolean; }) => {
  return (
    <div className={clsx("overflow-hidden flex flex-col rounded shadow bg-white mx-auto w-[min-content]", full && "w-full h-[100%]")}>
      {title && (
        <div className="border-b-[1px] border-gray-200 border-dashed px-6 py-4">
          <h2>{title}</h2>
        </div>
      )}
      <div className={clsx("h-full", innerPadding && "p-6")}>{children}</div>
    </div>
  );
};

export default Card;
