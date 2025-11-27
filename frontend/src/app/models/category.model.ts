export interface Category {
  id: number;
  name: string;
  description: string;
  image_url: string;
  parent_id?: number | null;
  created_at?: string;
  updated_at?: string;
  subcategories?: Category[];
}
