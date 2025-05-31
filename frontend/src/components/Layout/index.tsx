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
      <main className="flex flex-col flex-1 w-full h-[calc(100vh-60px)] justify-center items-center">
        <div className="container">
          {children}
        </div>
      </main>
    </>
  );
};

export default Layout;
