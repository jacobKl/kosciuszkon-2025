import { Canvas, useThree } from "@react-three/fiber";
import { useEffect } from "react";
import { OrbitControls } from "@react-three/drei";
import * as THREE from "three";

function CameraLookAtCenter() {
  const { camera } = useThree();
  useEffect(() => {
    camera.lookAt(0, 0, 0);
  }, [camera]);
  return null;
}

const HomeScene = () => {
  const home = {
    type: "Feature",
    properties: {
      height: 24,
    },
    geometry: {
      type: "Polygon",
      coordinates: [
        [19.905345, 50.0710032],
        [19.9053289, 50.071006],
        [19.9050098, 50.0702544],
        [19.9051902, 50.0702224],
        [19.9051916, 50.0702254],
        [19.9051847, 50.0702268],
        [19.9052905, 50.0704745],
        [19.9053486, 50.0706107],
        [19.9055661, 50.0711221],
        [19.905573, 50.0711212],
        [19.905574, 50.0711245],
        [19.9053931, 50.0711562],
        [19.9053492, 50.0710532],
        [19.9053654, 50.0710503],
        [19.905345, 50.0710032],
        [19.905345, 50.0710032],
      ],
    },
  };
  const { coordinates } = home.geometry;

  const [lon0, lat0] = coordinates[0];
  const scale = 50000;
  const flatPolygon = coordinates.map(([lon, lat]) => [
    (lon - lon0) * scale,
    (lat - lat0) * scale,
  ]);

  const shape = new THREE.Shape();
  flatPolygon.forEach(([x, y], i) => {
    if (i === 0) shape.moveTo(x, y);
    else shape.lineTo(x, y);
  });
  const geometry = new THREE.ShapeGeometry(shape);

  const PolygonMesh = () => {
    return (
      <mesh
        position={[0, 0.1, 0]}
        geometry={geometry}
        rotation={[-Math.PI / 2, 0, 0]}
      >
        <meshStandardMaterial color="orange" />
      </mesh>
    );
  };

  return (
    <div
      style={{ width: "100vw", height: "100vh", position: "fixed", inset: 0 }}
    >
      <Canvas className="w-full h-full" camera={{ position: [100, 100, 100] }}>
        <CameraLookAtCenter />
        <OrbitControls />
        {/* Ziemia */}
        <ambientLight />
        <PolygonMesh />
        <mesh rotation={[-Math.PI / 2, 0, 0]}>
          <planeGeometry args={[100, 100]} />
          <meshStandardMaterial color="#4C9F70" />
        </mesh>
      </Canvas>
    </div>
  );
};

export default HomeScene;
