import React from "react";
import { motion, useAnimation } from "framer-motion";
import { useEffect, useState } from "react";

const CountUp = ({ from = 0, to, duration = 2 } : {from: any; to: any; duration?: number}) => {
  const controls = useAnimation();
  const [count, setCount] = useState(from);

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
      onUpdate={(latest) => setCount(Math.floor(latest.count))}
    >
      {count}
    </motion.span>
  );
}

export default CountUp;
