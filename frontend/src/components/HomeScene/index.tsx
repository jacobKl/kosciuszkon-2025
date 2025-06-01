import { Canvas, useThree } from "@react-three/fiber";
import { useEffect } from "react";
import { OrbitControls } from "@react-three/drei";
import { AnimatePresence } from "framer-motion";

import House from "../House";
import GrassPlane from "../GrassPanel";
import CanvasLoader from "../CanvasLoader";

function CameraLookAtCenter() {
  const { camera } = useThree();
  useEffect(() => {
    camera.lookAt(0, 0, 0);
  }, [camera]);
  return null;
}

const HomeScene = ({ data, isLoading, isError, roofType, roofOrientation, solarAmount }: { data: any; isLoading: boolean; isError: boolean; roofType: string; roofOrientation: boolean; solarAmount: number; }) => {
  if (isError) return <div>Error</div>;

  return (
    <div className="w-full h-full relative">
      <AnimatePresence>
        {isLoading && <CanvasLoader />}
      </AnimatePresence>
      <div className="w-full h-full">
        <Canvas className="w-full h-full" camera={{ position: [0, 40, 0] }} shadows>
          <CameraLookAtCenter />
          <OrbitControls minDistance={10} maxDistance={50} />
          {data?.features.map((feature, index) => (
            <House key={`house${index}`} solarAmount={solarAmount} house={feature} data={data} roofType={roofType} roofOrientation={roofOrientation} />
          ))}
          <directionalLight position={[100, 200, 100]} intensity={1} castShadow shadow-mapSize-width={2048} shadow-mapSize-height={2048} />
          <directionalLight
            castShadow
            position={[100, 200, 100]}
            intensity={1.5}
            color="#fff8dc"
            shadow-mapSize-width={2048}
            shadow-mapSize-height={2048}
            shadow-camera-left={-50}
            shadow-camera-right={50}
            shadow-camera-top={50}
            shadow-camera-bottom={-50}
            shadow-camera-near={1}
            shadow-camera-far={500}
          />

          <GrassPlane />

          <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
            <meshStandardMaterial color="#4C9F70" />
          </mesh>
        </Canvas>
      </div>
    </div>
  );
};

export default HomeScene;
