import React, { type ReactNode } from "react";

const Card = ({ children, title }: { children: ReactNode; title: string }) => {
  return (
    <div className="rounded shadow bg-white min-h-[300px] mx-auto w-[min-content]">
      {title && (
        <div className="border-b-[1px] border-gray-200 border-dashed px-6 py-4">
          <h2>{title}</h2>
        </div>
      )}
      <div className="p-6">{children}</div>
    </div>
  );
};

export default Card;
