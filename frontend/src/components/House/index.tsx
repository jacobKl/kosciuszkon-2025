import { useLoader } from "@react-three/fiber";
import * as THREE from "three";
import type {
  AddressFeatureCollection,
  AddressFeature,
} from "../../types/address";

const createShape = (coords: number[][]) => {
  const s = new THREE.Shape();
  coords.forEach(([x, y], i) => {
    if (i === 0) s.moveTo(x, y);
    else s.lineTo(x, y);
  });
  return s;
};

const House = ({
  house,
  data,
}: {
  house: AddressFeature;
  data: AddressFeatureCollection;
}) => {
  const wallColorTexture = useLoader(
    THREE.TextureLoader,
    "/textures/bricks/color.jpg",
  );
  const wallAOTexture = useLoader(
    THREE.TextureLoader,
    "/textures/bricks/ambient.jpg",
  );
  const wallNormalTexture = useLoader(
    THREE.TextureLoader,
    "/textures/bricks/normal.jpg",
  );
  wallColorTexture.colorSpace = THREE.SRGBColorSpace;

  wallColorTexture.wrapS = wallColorTexture.wrapT = THREE.RepeatWrapping;
  wallAOTexture.wrapS = wallAOTexture.wrapT = THREE.RepeatWrapping;
  wallNormalTexture.wrapS = wallNormalTexture.wrapT = THREE.RepeatWrapping;

  const { coordinates } = house.geometry;
  const houseShape = createShape(coordinates[0]);
  const houseGeometry = new THREE.ExtrudeGeometry(houseShape, {
    steps: 1,
    depth: 10,
    bevelEnabled: false,
  });
  houseGeometry.computeBoundingBox();
  // @ts-ignore
  const { min, max } = houseGeometry?.boundingBox;
  const offset = new THREE.Vector2(0 - min.x, 0 - min.y);
  const range = new THREE.Vector2(max.x - min.x, max.y - min.y);
  const housePositions = houseGeometry.attributes.position;
  const houseUvs = [];

  // UV skalowane do rzeczywistych wymiarów ściany, aby tekstura cegieł była powtarzana proporcjonalnie
  const uvScale = 0.25; // 1 cegła co 0.25 jednostki, dostosuj do rozmiaru tekstury
  for (let i = 0; i < housePositions.count; i++) {
    const v3 = new THREE.Vector3().fromBufferAttribute(housePositions, i);
    houseUvs.push((v3.x + offset.x) * uvScale);
    houseUvs.push((v3.y + offset.y) * uvScale);
  }
  houseGeometry.setAttribute(
    "uv",
    new THREE.BufferAttribute(new Float32Array(houseUvs), 2),
  );
  houseGeometry.setAttribute(
    "uv2",
    new THREE.BufferAttribute(new Float32Array(houseUvs), 2),
  );
  houseGeometry.attributes.uv.needsUpdate = true;
  houseGeometry.attributes.uv2.needsUpdate = true;

  const { hip } = house?.properties?.roof_3d_polygons;
  if (!hip) return <></>;

  const geometries = Object.values(hip).map((verticies) => {
    const verts = verticies.flat().flat();
    const geometry = new THREE.BufferGeometry();

    const roofVerticies = new Float32Array(verts);

    geometry.setAttribute(
      "position",
      new THREE.BufferAttribute(roofVerticies, 3),
    );
    return geometry;
  });

  return (
    <>
      <mesh
        rotation={[Math.PI / 2, 0, 0]}
        position={[0, house.properties.height, 0]}
        geometry={houseGeometry}
        castShadow
      >
        <meshStandardMaterial
          color="orange"
          side={THREE.DoubleSide}
          map={wallColorTexture}
          aoMap={wallAOTexture}
          roughnessMap={wallAOTexture}
          metalnessMap={wallAOTexture}
          normalMap={wallNormalTexture}
        />
      </mesh>
      <mesh position={[0, 0, 0]} geometry={geometries[0]} castShadow>
        <meshStandardMaterial color="red" side={THREE.DoubleSide} />
      </mesh>
    </>
  );
};

export default House;
