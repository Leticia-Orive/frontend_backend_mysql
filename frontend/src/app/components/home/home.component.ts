import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CategoryService } from '../../services/category.service';
import { ProductService } from '../../services/product.service';
import { Category } from '../../models/category.model';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent implements OnInit {
  currentUser: any = null;
  categories: Category[] = [];
  productsByCategory: { [key: number]: Product[] } = {};
  loading = true;
  error: string | null = null;
  selectedCategory: number | null = null;

  constructor(
    private authService: AuthService,
    private categoryService: CategoryService,
    private productService: ProductService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });
    this.loadCategories();
  }

  loadCategories(): void {
    this.loading = true;
    this.categoryService.getCategories().subscribe({
      next: (categories) => {
        this.categories = categories;
        this.loadAllProducts();
      },
      error: (err) => {
        this.error = 'Error al cargar las categorías';
        this.loading = false;
      }
    });
  }

  loadAllProducts(): void {
    this.productService.getProducts().subscribe({
      next: (products) => {
        // Agrupar productos por categoría
        this.categories.forEach(category => {
          this.productsByCategory[category.id] = products.filter(
            p => p.category_id === category.id
          );
        });
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los productos';
        this.loading = false;
      }
    });
  }

  filterByCategory(categoryId: number | null): void {
    this.selectedCategory = categoryId;
  }

  getFilteredCategories(): Category[] {
    if (this.selectedCategory === null) {
      return this.categories;
    }
    return this.categories.filter(c => c.id === this.selectedCategory);
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/login']);
  }

  goToUsers(): void {
    if (this.currentUser?.role === 'admin') {
      this.router.navigate(['/users']);
    }
  }
}
