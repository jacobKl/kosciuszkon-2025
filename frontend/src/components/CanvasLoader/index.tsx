import { motion } from "framer-motion";

const CanvasLoader = () => (
  <motion.div
    className="absolute inset-0 flex items-center justify-center bg-white z-50"
    initial={{ opacity: 1 }}
    animate={{ opacity: 1 }}
    exit={{ opacity: 0 }}
    transition={{ duration: 0.5 }}
  >
    <motion.div
      animate={{ rotate: 360 }}
      transition={{ repeat: Infinity, duration: 1, ease: "linear" }}
      style={{
        width: 48,
        height: 48,
        border: "6px solid #4C9F70",
        borderTop: "6px solid #fff",
        borderRadius: "50%",
      }}
    />
  </motion.div>
);

export default CanvasLoader;