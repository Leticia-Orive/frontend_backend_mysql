import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { ProductService } from '../../services/product.service';
import { CategoryService } from '../../services/category.service';
import { AuthService } from '../../services/auth.service';
import { Product } from '../../models/product.model';
import { Category } from '../../models/category.model';

@Component({
  selector: 'app-subcategory-products',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './subcategory-products.component.html',
  styleUrl: './subcategory-products.component.css'
})
export class SubcategoryProductsComponent implements OnInit {
  subcategoryId: number = 0;
  subcategory: Category | null = null;
  products: Product[] = [];
  loading = true;
  error: string | null = null;
  currentUser: any = null;
  cart: { product: Product; quantity: number }[] = [];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private productService: ProductService,
    private categoryService: CategoryService,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
    });

    this.route.params.subscribe(params => {
      this.subcategoryId = +params['id'];
      this.loadSubcategory();
      this.loadProducts();
    });
  }

  loadSubcategory(): void {
    this.categoryService.getCategory(this.subcategoryId, false).subscribe({
      next: (category) => {
        this.subcategory = category;
      },
      error: (err) => {
        this.error = 'Error al cargar la subcategoría';
      }
    });
  }

  loadProducts(): void {
    this.productService.getProductsByCategory(this.subcategoryId).subscribe({
      next: (products) => {
        this.products = products;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar los productos';
        this.loading = false;
      }
    });
  }

  addToCart(product: Product): void {
    if (product.stock === 0) {
      return;
    }

    const existingItem = this.cart.find(item => item.product.id === product.id);
    
    if (existingItem) {
      if (existingItem.quantity < product.stock) {
        existingItem.quantity++;
      } else {
        alert('No hay más stock disponible');
      }
    } else {
      this.cart.push({ product, quantity: 1 });
    }
    
    alert('Producto añadido al carrito');
  }

  goBack(): void {
    this.router.navigate(['/home']);
  }

  isAdmin(): boolean {
    return this.currentUser?.role === 'admin';
  }
}
