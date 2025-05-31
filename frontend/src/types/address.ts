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
  };
  geometry: {
    type: "Polygon";
    coordinates: number[][][]; // [[[lon, lat], ...]]
  };
};
