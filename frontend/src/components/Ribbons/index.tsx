import { motion } from "framer-motion";

const Ribbons = () => {
  const getVariants = (fromLeft = true) => ({
    hidden: { x: fromLeft ? -700 : 700, delay: 2 + Math.random() * 5 * 0.1 },
    visible: {
      x: 0,
      transition: { type: "spring", stiffness: 120, damping: 14 },
    },
  });

  return (
    <svg
      width="7676"
      height="2188"
      viewBox="0 0 7676 2188"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="ribbons"
    >
      {/* Right side rectangle — zip in from right */}
      <motion.path
        d="M6891.83 824.722L9267.03 527.726V889.661L6891.83 1186.66V824.722Z"
        fill="#4C9F70"
        variants={getVariants(false)} // from right
        initial="hidden"
        animate="visible"
      />
      <motion.path
        d="M4448.77 772.712L7909.78 338.343V700.278L4448.77 1134.65V772.712Z"
        fill="#4C9F70"
        fillOpacity="0.4"
        variants={getVariants(false)} // from right
        initial="hidden"
        animate="visible"
        transition={{ delay: 0.1, type: "spring", stiffness: 130, damping: 15 }}
      />
      <motion.path
        d="M5353.61 297.156L7728.81 0.159912V362.095L5353.61 659.091V297.156Z"
        fill="#4C9F70"
        variants={getVariants(false)} // from right
        initial="hidden"
        animate="visible"
        transition={{ delay: 0.2, type: "spring", stiffness: 140, damping: 16 }}
      />
      {/* Left side rectangles — zip in from left */}
      <motion.path
        d="M-233.768 1356.38L2141.43 1059.38V1421.32L-233.768 1718.31V1356.38Z"
        fill="#496F5D"
        fillOpacity="0.4"
        variants={getVariants(true)} // from left
        initial="hidden"
        animate="visible"
        transition={{ delay: 0.3, type: "spring", stiffness: 150, damping: 17 }}
      />
      <motion.path
        d="M-1093.36 1825.7L1281.84 1528.7V1890.64L-1093.36 2187.63V1825.7Z"
        fill="#4C9F70"
        fillOpacity="0.7"
        variants={getVariants(true)} // from left
        initial="hidden"
        animate="visible"
        transition={{ delay: 0.4, type: "spring", stiffness: 160, damping: 18 }}
      />
    </svg>
  );
}

export default Ribbons;