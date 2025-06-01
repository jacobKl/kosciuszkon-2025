import { useLoader } from "@react-three/fiber";
import * as THREE from "three";

const GrassPlane = () => {
  const grassTexture = useLoader(THREE.TextureLoader, "/grass.jpg");
  const grassNormal = useLoader(THREE.TextureLoader, "/grass_normal.jpg");
  const grassDisplacement = useLoader(THREE.TextureLoader, "/grass_displacement.jpg");

  grassTexture.wrapS = grassTexture.wrapT = THREE.RepeatWrapping;
  grassNormal.wrapS = grassNormal.wrapT = THREE.RepeatWrapping;
  grassDisplacement.wrapS = grassDisplacement.wrapT = THREE.RepeatWrapping;

  grassTexture.repeat.set(10, 10);
  grassNormal.repeat.set(10, 10);
  grassDisplacement.repeat.set(10, 10);

  return (
    <mesh rotation={[-Math.PI / 2, 0, 0]} receiveShadow>
      <planeGeometry args={[300, 300, 256, 256]} />
      <meshStandardMaterial
        map={grassTexture}
        normalMap={grassNormal}
        displacementMap={grassDisplacement}
        displacementScale={0.5}
      />
    </mesh>
  );
};

export default GrassPlane;
