import React from "react";
import { motion, useAnimation } from "framer-motion";
import { useEffect, useState } from "react";

const CountUp = ({ from = 0, to, duration = 2 }: { from?: number; to: number; duration?: number }) => {
  const controls = useAnimation();
  const [count, setCount] = useState(from);

  const isFloat = to % 1 !== 0;

  useEffect(() => {
    controls.start({
      count: to,
      transition: { duration: duration, ease: "easeOut" },
    });
  }, [to, controls, duration]);

  return (
    <motion.span
      animate={controls}
      initial={{ count: from }}
      onUpdate={(latest) => {
        const current = latest.count;
        if (isFloat) {
          setCount(parseFloat(current.toFixed(2)));
        } else {
          setCount(Math.floor(current));
        }
      }}
    >
      {count}
    </motion.span>
  );
};

export default CountUp;
