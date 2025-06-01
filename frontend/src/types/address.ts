export type AddressFeatureCollection = {
  type: "FeatureCollection";
  features: AddressFeature[];
  properties: {
    average_centroid: {
      lat: number;
      lon: number;
    };
    address: string;
    garages_found: number;
  };
};

export type AddressFeature = {
  type: "Feature";
  properties: {
    height: number;
    addr_street: string;
    addr_housenumber: string;
    roof_3d_polygons: {
      flat: { "1": number[][]; "2": number[][] };
      gable: { "1": number[][]; "2": number[][] };
      hip: { "1": number[][]; "2": number[][] };
    };
  };
  geometry: {
    type: "Polygon";
    coordinates: number[][][]; // [[[lon, lat], ...]]
  };
};
