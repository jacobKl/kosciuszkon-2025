import * as THREE from "three";
import type {
  AddressFeatureCollection,
  AddressFeature,
} from "../../types/address";

const House = ({
  house,
  data,
}: {
  house: AddressFeature;
  data: AddressFeatureCollection;
}) => {
  const { flat } = house?.properties?.roof_3d_polygons;
  if (!flat) return <></>;

  const geometries = Object.values(flat).map((verticies) => {
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
      <mesh position={[0, 0, 0]} geometry={geometries[0]} castShadow>
        <meshStandardMaterial color="orange" side={THREE.DoubleSide} />
      </mesh>
    </>
  );
};

export default House;
