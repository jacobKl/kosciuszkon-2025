import { useLoader } from "@react-three/fiber";
import * as THREE from "three";
import type { AddressFeatureCollection, AddressFeature } from "../../types/address";

const createShape = (coords: number[][]) => {
  const s = new THREE.Shape();
  coords.forEach(([x, y], i) => {
    if (i === 0) s.moveTo(x, y);
    else s.lineTo(x, y);
  });
  return s;
};

const House = ({ house, data, roofType, roofOrientation, solarAmount = 1 }: { house: AddressFeature; data: AddressFeatureCollection; roofType: string; roofOrientation: boolean; solarAmount: number; }) => {
  const { coordinates } = house.geometry;
  const houseShape = createShape(coordinates[0]);

  const houseGeometry = new THREE.ExtrudeGeometry(houseShape, {
    steps: 1,
    depth: house.properties.height,
    bevelEnabled: false,
  });

  houseGeometry.computeBoundingBox();
  const { min, max } = houseGeometry.boundingBox!;
  const offset = new THREE.Vector2(-min.x, -min.y);

  const housePositions = houseGeometry.attributes.position;
  const houseUvs: number[] = [];
  const uvScale = 0.25;

  for (let i = 0; i < housePositions.count; i++) {
    const v3 = new THREE.Vector3().fromBufferAttribute(housePositions, i);
    houseUvs.push((v3.x + offset.x) * uvScale);
    houseUvs.push((v3.y + offset.y) * uvScale);
  }

  houseGeometry.setAttribute("uv", new THREE.BufferAttribute(new Float32Array(houseUvs), 2));
  houseGeometry.setAttribute("uv2", new THREE.BufferAttribute(new Float32Array(houseUvs), 2));
  houseGeometry.attributes.uv.needsUpdate = true;
  houseGeometry.attributes.uv2.needsUpdate = true;

  let roofMesh = null;

  if (roofType === "flat") {
    const flatRoofGeometry = new THREE.ExtrudeGeometry(houseShape, {
      steps: 1,
      depth: 0.3,
      bevelEnabled: false,
    });

    flatRoofGeometry.computeVertexNormals();

    roofMesh = (
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, house.properties.height + 0.3, 0]} geometry={flatRoofGeometry} castShadow>
        <meshStandardMaterial color="gray" side={THREE.DoubleSide} />
        
        {house.properties?.solar_panels?.flat?.coordinates?.slice(0, solarAmount)?.map(
        (triangle: number[][][], index: number) => {
          const flatVerts = triangle.flat().flat(); // flatten to Float32Array
          const geometry = new THREE.BufferGeometry();
          geometry.setAttribute(
            "position",
            new THREE.BufferAttribute(new Float32Array(flatVerts), 3)
          );
          geometry.computeVertexNormals();

          return (
            <mesh
              key={`solar-${index}`}
              position={[0, 0.01, 0]}
              rotation={[Math.PI / 2, 0, 0]}
              geometry={geometry}
              castShadow
            >
              <meshStandardMaterial color="#222" side={THREE.DoubleSide} />
            </mesh>
          );
        }
      )}
      </mesh>
    );
  } else if (roofType === 'gable') {
    const roofVertices = house?.properties?.roof_3d_polygons?.gable;

    const geometries = Object.values(roofVertices).map((verticies) => {
      const verts = verticies.flat().flat();
      const geometry = new THREE.BufferGeometry();

      geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(new Float32Array(verts), 3)
      );
      geometry.computeVertexNormals();

      return geometry;
    });

    roofMesh = (
      <mesh position={[0, 0, 0]} geometry={geometries[roofOrientation]} castShadow>
        <meshStandardMaterial color="gray" side={THREE.DoubleSide} />
      </mesh>
    );
  } else {
    const roofVertices = house?.properties?.roof_3d_polygons?.hip;

    const geometries = Object.values(roofVertices).map((verticies) => {
      const verts = verticies.flat().flat();
      const geometry = new THREE.BufferGeometry();

      geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(new Float32Array(verts), 3)
      );
      geometry.computeVertexNormals();

      return geometry;
    });

    roofMesh = (
      <mesh position={[0, 0, 0]} geometry={geometries[roofOrientation]} castShadow>
        <meshStandardMaterial color="gray" side={THREE.DoubleSide} />
      </mesh>
    );
  }

  return (
    <>
      <mesh rotation={[Math.PI / 2, 0, 0]} position={[0, house.properties.height, 0]} geometry={houseGeometry} castShadow>
        <meshStandardMaterial
          color="#FAF0CA"
          side={THREE.DoubleSide}
        />
      </mesh>

      {roofMesh}
    </>
  );
};

export default House;
