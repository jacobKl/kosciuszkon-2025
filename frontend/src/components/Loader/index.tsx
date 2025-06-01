import { useEffect, useState } from "react";
import { motion, useAnimation } from "framer-motion";

const Loader = () => {
  const [text, setText] = useState("");
  const [isSplitting, setIsSplitting] = useState(false);
  const fullText = "GreenHouse";
  const controls = useAnimation();

  useEffect(() => {
    let index = 0;
    const interval = setInterval(() => {
      setText(fullText.slice(0, index + 1));
      index++;
      if (index === fullText.length) {
        clearInterval(interval);
        setTimeout(() => {
          setIsSplitting(true);
          controls.start("split");
        }, 200);
      }
    }, 100);
    return () => clearInterval(interval);
  }, []);

  const leftVariants = {
    initial: { x: 0, border: "none" },
    split: { x: "-100vw", transition: { duration: 1, ease: "easeInOut" } },
  };

  const overlayVariants = {
    initial: { opacity: 1 },
    split: { opacity: 0, transition: { delay: 1, duration: 0.5 } },
  };

  return (
    <motion.div
      className="fixed inset-0 bg-white overflow-hidden z-50 pointer-events-none"
      initial="initial"
      animate={controls}
      variants={overlayVariants}
    >
      <motion.div
        className="absolute left-0 top-0 w-full h-full bg-primary flex justify-center items-center select-none font-mono font-bold text-4xl overflow-hidden"
        variants={leftVariants}
      >
      </motion.div>

      <motion.div
        className="fixed inset-0 flex justify-center items-center pointer-events-none select-none font-thin text-4xl text-white z-10"
        initial={{ opacity: 1 }}
        animate={{ opacity: isSplitting ? 0 : 1 }}
        transition={{ duration: 0.3 }}
      >
        {text}
      </motion.div>
    </motion.div>
  );
}

export default Loader;