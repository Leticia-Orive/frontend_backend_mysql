import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category } from '../models/category.model';

@Injectable({
  providedIn: 'root'
})
export class CategoryService {
  private apiUrl = 'http://localhost:5000/api/categories';

  constructor(private http: HttpClient) { }

  getCategories(includeSubcategories: boolean = false): Observable<Category[]> {
    const params = includeSubcategories ? '?include_subcategories=true' : '';
    return this.http.get<Category[]>(`${this.apiUrl}${params}`);
  }

  getCategory(id: number, includeSubcategories: boolean = true): Observable<Category> {
    const params = includeSubcategories ? '?include_subcategories=true' : '?include_subcategories=false';
    return this.http.get<Category>(`${this.apiUrl}/${id}${params}`);
  }

  getSubcategories(categoryId: number): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.apiUrl}/${categoryId}/subcategories`);
  }
}
