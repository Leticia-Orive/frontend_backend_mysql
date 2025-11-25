import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CategoryService } from '../../services/category.service';
import { ProductService } from '../../services/product.service';
import { Category } from '../../models/category.model';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
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
  
  // Product form
  showProductForm = false;
  isEditingProduct = false;
  currentProduct: Partial<Product> = {};
  
  // Cart
  cart: { product: Product; quantity: number }[] = [];
  cartTotal = 0;
  showCart = false;

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
    this.loadCart();
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

  // Admin functions
  isAdmin(): boolean {
    return this.currentUser?.role === 'admin';
  }

  openCreateProductForm(): void {
    this.showProductForm = true;
    this.isEditingProduct = false;
    this.currentProduct = {
      name: '',
      description: '',
      price: 0,
      stock: 0,
      image_url: '',
      category_id: this.categories[0]?.id || 1
    };
  }

  openEditProductForm(product: Product): void {
    this.showProductForm = true;
    this.isEditingProduct = true;
    this.currentProduct = { ...product };
  }

  closeProductForm(): void {
    this.showProductForm = false;
    this.currentProduct = {};
  }

  saveProduct(): void {
    if (!this.currentProduct.name || !this.currentProduct.price || !this.currentProduct.category_id) {
      alert('Por favor completa todos los campos requeridos');
      return;
    }

    if (this.isEditingProduct && this.currentProduct.id) {
      this.productService.updateProduct(this.currentProduct.id, this.currentProduct).subscribe({
        next: () => {
          this.loadAllProducts();
          this.closeProductForm();
        },
        error: (err) => {
          this.error = 'Error al actualizar el producto';
        }
      });
    } else {
      this.productService.createProduct(this.currentProduct).subscribe({
        next: () => {
          this.loadAllProducts();
          this.closeProductForm();
        },
        error: (err) => {
          this.error = 'Error al crear el producto';
        }
      });
    }
  }

  deleteProduct(product: Product): void {
    if (confirm(`¿Estás seguro de que quieres eliminar "${product.name}"?`)) {
      this.productService.deleteProduct(product.id).subscribe({
        next: () => {
          this.loadAllProducts();
        },
        error: (err) => {
          this.error = 'Error al eliminar el producto';
        }
      });
    }
  }

  // Cart functions
  addToCart(product: Product): void {
    const existingItem = this.cart.find(item => item.product.id === product.id);
    
    if (existingItem) {
      if (existingItem.quantity < product.stock) {
        existingItem.quantity++;
      } else {
        alert('No hay más stock disponible');
        return;
      }
    } else {
      this.cart.push({ product, quantity: 1 });
    }
    
    this.saveCart();
    this.calculateTotal();
    alert(`${product.name} añadido al carrito`);
  }

  removeFromCart(index: number): void {
    this.cart.splice(index, 1);
    this.saveCart();
    this.calculateTotal();
  }

  updateQuantity(index: number, quantity: number): void {
    if (quantity > 0 && quantity <= this.cart[index].product.stock) {
      this.cart[index].quantity = quantity;
      this.saveCart();
      this.calculateTotal();
    }
  }

  calculateTotal(): void {
    this.cartTotal = this.cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
  }

  saveCart(): void {
    localStorage.setItem('cart', JSON.stringify(this.cart));
  }

  loadCart(): void {
    const savedCart = localStorage.getItem('cart');
    if (savedCart) {
      this.cart = JSON.parse(savedCart);
      this.calculateTotal();
    }
  }

  clearCart(): void {
    this.cart = [];
    this.saveCart();
    this.calculateTotal();
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
