import React from "react";
import { AnimatePresence, motion } from "framer-motion";

import {
  useAppContext,
  type AppContextType,
} from "../../context/AppContextProvider";
import AddressForm from "../AddressForm";
import clsx from "clsx";
import RoofForm from "../RoofForm";
import DetailedForm from "../DetailedForm";

const Steps = () => {
  const { step }: AppContextType = useAppContext();

  const variants = {
    initial: { opacity: 0, x: 50 },
    animate: { opacity: 1, x: 0 },
    exit: { opacity: 0, x: -50 },
  };

  const StepContent = () => {
    switch (step) {
      case 1:
        return <AddressForm />;
      case 2:
        return <RoofForm />;
      case 3: 
        return <DetailedForm />;
      default:
        return null;
    }
  };

  return (
    <>
      <div className="flex mb-4 gap-6 justify-center items-center">
        {[1, 2, 3].map((single, ix) => (
          <React.Fragment key={ix}>
            <div
              className={clsx(
                "p-4 transition-all font-thin bg-gray-100 shadow rounded-[25px] w-[50px] h-[50px] flex justify-center items-center",
                single <= step && "bg-primary text-white",
              )}
            >
              {single}
            </div>
            {single < 3 && (
              <div
                className={clsx(
                  "transition-all w-[100px] h-[4px] rounded-[1px] bg-gray-100",
                  single + 1 <= step && "bg-primary text-white",
                )}
              ></div>
            )}
          </React.Fragment>
        ))}
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key={step}
          variants={variants}
          initial="initial"
          animate="animate"
          exit="exit"
          transition={{ duration: 0.3 }}
          className="mb-6"
        >
          <StepContent />
        </motion.div>
      </AnimatePresence>
    </>
  );
};

export default Steps;
