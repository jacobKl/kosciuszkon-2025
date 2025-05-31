import React, { type ReactNode } from "react";
import Header from "../Header";
import Ribbons from "../Ribbons";
import Loader from "../Loader";

const Layout = ({ children }: { children?: ReactNode }) => {
  return (
    <>
      <Ribbons />
      {/* <Loader /> */}
      <Header />
      <main className="container mx-auto flex justify-center align-center flex-col min-h-[calc(100vh - 60px)] py-4">
        {children}
      </main>
    </>
  );
};

export default Layout;
