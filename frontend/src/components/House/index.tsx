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
  const { coordinates } = house.geometry;
  const houseShape = createShape(coordinates[0]);
  const houseGeometry = new THREE.ExtrudeGeometry(houseShape, {
    steps: 1,
    depth: 10,
    bevelEnabled: false,
  });

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
        <meshStandardMaterial color="orange" side={THREE.DoubleSide} />
      </mesh>
      <mesh position={[0, 0, 0]} geometry={geometries[0]} castShadow>
        <meshStandardMaterial color="red" side={THREE.DoubleSide} />
      </mesh>
    </>
  );
};

export default House;
