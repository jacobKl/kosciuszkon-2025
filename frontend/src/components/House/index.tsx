import * as THREE from "three";
import type {
  AddressFeatureCollection,
  AddressFeature,
} from "../../types/address";
import { Pane } from "tweakpane";
import { useMemo, useRef, useState, useEffect } from "react";

const House = ({
  home,
  data,
}: {
  home: AddressFeature;
  data: AddressFeatureCollection;
}) => {
  const [extrudeOptions, setExtrudeOptions] = useState({
    steps: 2,
    depth: home.properties.height,
    bevelEnabled: false,
    bevelSegments: 1,
    bevelSize: home.properties.height / 2,
    bevelThickness: home.properties.height / 2,
    bevelOffset: 0,
  });

  const paneRef = useRef<Pane>(null);
  useEffect(() => {
    if (!paneRef.current) {
      paneRef.current = new Pane();
      Object.keys(extrudeOptions).forEach((key) => {
        paneRef
          // @ts-ignore
          .current!.addBinding(extrudeOptions, key, {
            min: -20,
            max: 20,
            step: 1,
          })
          .on("change", (ev) => {
            setExtrudeOptions((opts) => ({
              ...opts,
              [key]: ev.value,
            }));
          });
      });
    }
    return () => {
      paneRef.current?.dispose();
    };
    // eslint-disable-next-line
  }, []);

  const { coordinates } = home.geometry;

  const [lon0, lat0] = coordinates[0][0];
  const center = {
    lat: data?.properties.average_centroid.lat || lat0,
    lon: data?.properties.average_centroid.lon || lon0,
  };
  const scale = 50000;
  const flatPolygon = coordinates[0].map(([lon, lat]) => [
    (lon - center.lon) * scale,
    (lat - center.lat) * scale,
  ]);

  const shape = useMemo(() => {
    const s = new THREE.Shape();
    flatPolygon.forEach(([x, y], i) => {
      if (i === 0) s.moveTo(x, y);
      else s.lineTo(x, y);
    });
    return s;
  }, [flatPolygon]);

  const houseGeometry = useMemo(
    () => new THREE.ExtrudeGeometry(shape, extrudeOptions),
    [shape, extrudeOptions],
  );

  return (
    <mesh
      position={[0, 0.1, 0]}
      geometry={houseGeometry}
      rotation={[-Math.PI / 2, 0, 0]}
      castShadow
    >
      <meshStandardMaterial color="orange" />
    </mesh>
  );
};

export default House;
