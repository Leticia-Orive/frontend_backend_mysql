export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  stock: number;
  image_url: string;
  category_id: number;
  category_name?: string;
  created_at?: string;
  updated_at?: string;
}
