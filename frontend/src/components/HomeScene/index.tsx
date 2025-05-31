import { Canvas, useThree } from "@react-three/fiber";
import { useEffect } from "react";
import { OrbitControls } from "@react-three/drei";
import { useAddressQuery } from "../../queries/useAddressQuery";
import { useAppContext } from "../../context/AppContextProvider";
import House from "../House";

function CameraLookAtCenter() {
  const { camera } = useThree();
  useEffect(() => {
    camera.lookAt(0, 0, 0);
  }, [camera]);
  return null;
}

const HomeScene = () => {
  const { formState } = useAppContext();

  const { data, isError, isLoading } = useAddressQuery(formState);

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error</div>;

  return (
    <div className="w-full h-full">
      <Canvas
        className="w-full h-full"
        camera={{ position: [0, 40, 0] }}
        shadows
      >
        <CameraLookAtCenter />
        <OrbitControls />
        {data?.features.map((feature, index) => (
          <House key={`house${index}`} home={feature} data={data} />
        ))}
        {/* Światło rzucające cień */}
        <directionalLight
          position={[100, 200, 100]}
          intensity={1}
          castShadow
          shadow-mapSize-width={2048}
          shadow-mapSize-height={2048}
        />
        <ambientLight intensity={0.3} />
        <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
          <planeGeometry args={[100, 100]} />
          <meshStandardMaterial color="#4C9F70" />
        </mesh>
      </Canvas>
    </div>
  );
};

export default HomeScene;
