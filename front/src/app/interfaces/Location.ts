export interface Location {
  slug: string;
  location: {
    external_id: string;
  };
  label: string;
  uuid: string;
  centroid?: any[];
  geometry?: any;
}