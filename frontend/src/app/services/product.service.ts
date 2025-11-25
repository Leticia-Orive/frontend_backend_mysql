import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../models/product.model';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class ProductService {
  private apiUrl = 'http://localhost:5000/api/products';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) { }

  getProducts(categoryId?: number): Observable<Product[]> {
    const url = categoryId 
      ? `${this.apiUrl}?category_id=${categoryId}` 
      : this.apiUrl;
    return this.http.get<Product[]>(url);
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/${id}`);
  }

  getProductsByCategory(categoryId: number): Observable<Product[]> {
    return this.http.get<Product[]>(`http://localhost:5000/api/categories/${categoryId}/products`);
  }

  createProduct(product: Partial<Product>): Observable<any> {
    return this.http.post(this.apiUrl, product, {
      headers: this.authService.getAuthHeaders()
    });
  }

  updateProduct(id: number, product: Partial<Product>): Observable<any> {
    return this.http.put(`${this.apiUrl}/${id}`, product, {
      headers: this.authService.getAuthHeaders()
    });
  }

  deleteProduct(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/${id}`, {
      headers: this.authService.getAuthHeaders()
    });
  }
}
