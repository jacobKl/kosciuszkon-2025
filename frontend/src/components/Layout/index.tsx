import React from "react";
import Header from "../Header";
import Ribbons from "../Ribbons";

const Layout = ({ children }) => {
  return (
    <>
      <Header />
      <main className="container mx-auto flex justify-center align-center flex-col min-h-[calc(100vh - 60px)] py-4">{children}</main>;
      <Ribbons />
    </>
  );
};

export default Layout;
