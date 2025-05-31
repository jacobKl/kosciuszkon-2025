import React from "react";

const Card = ({ children }) => {
  return <div className="p-6 rounded shadow bg-white min-h-[300px] mx-auto w-[min-content]">{children}</div>;
};

export default Card;
