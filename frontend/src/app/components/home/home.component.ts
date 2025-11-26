import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { CategoryService } from '../../services/category.service';
import { ProductService } from '../../services/product.service';
import { CouponService } from '../../services/coupon.service';
import { Category } from '../../models/category.model';
import { Product } from '../../models/product.model';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
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
  cartSubtotal = 0;
  cartDiscount = 0;
  showCart = false;
  
  // Discounts and coupons
  userDiscount = 0.10; // 10% discount for registered users
  couponCode = '';
  appliedCoupon: string | null = null;
  couponDiscount = 0;
  userCoupons: any[] = [];
  showCouponsNotification = false;
  
  // Product detail view
  showProductDetail = false;
  selectedProduct: Product | null = null;

  constructor(
    private authService: AuthService,
    private categoryService: CategoryService,
    private productService: ProductService,
    private couponService: CouponService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      if (user) {
        this.loadUserCoupons();
      }
    });
    this.loadCategories();
    // No cargar el carrito automáticamente
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

  // Product detail functions
  viewProduct(product: Product): void {
    this.selectedProduct = product;
    this.showProductDetail = true;
  }

  closeProductDetail(): void {
    this.showProductDetail = false;
    this.selectedProduct = null;
  }

  addToCartFromDetail(): void {
    if (this.selectedProduct) {
      this.addToCart(this.selectedProduct);
      this.closeProductDetail();
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
    this.cartSubtotal = this.cart.reduce((sum, item) => sum + (item.product.price * item.quantity), 0);
    
    // Apply discount for registered users
    if (this.currentUser) {
      this.cartDiscount = this.cartSubtotal * this.userDiscount;
    } else {
      this.cartDiscount = 0;
    }
    
    // Apply coupon discount
    let couponAmount = 0;
    if (this.appliedCoupon) {
      couponAmount = this.couponDiscount;
    }
    
    this.cartTotal = this.cartSubtotal - this.cartDiscount - couponAmount;
  }

  saveCart(): void {
    // No guardar en localStorage
  }

  loadCart(): void {
    // Cart no se carga automáticamente desde localStorage
    this.cart = [];
    this.calculateTotal();
  }

  clearCart(): void {
    this.cart = [];
    this.saveCart();
    this.calculateTotal();
  }

  loadUserCoupons(): void {
    this.couponService.getMyCoupons().subscribe({
      next: (coupons) => {
        this.userCoupons = coupons;
        if (coupons.length > 0) {
          this.showCouponsNotification = true;
        }
      },
      error: (err) => {
        console.error('Error al cargar cupones:', err);
      }
    });
  }

  applyCoupon(): void {
    if (!this.couponCode.trim()) {
      alert('Por favor ingresa un código de cupón');
      return;
    }

    // Buscar el cupón en los cupones del usuario
    const userCoupon = this.userCoupons.find(c => c.coupon_code === this.couponCode.trim());
    
    if (userCoupon) {
      if (this.currentUser) {
        // Usuario registrado usando su cupón personal
        this.couponService.useCoupon(this.couponCode).subscribe({
          next: (response) => {
            this.appliedCoupon = this.couponCode;
            this.couponDiscount = response.discount_amount;
            this.calculateTotal();
            this.loadUserCoupons(); // Recargar cupones
            alert(`¡Cupón aplicado! Descuento de €${this.couponDiscount}`);
          },
          error: (err) => {
            alert('Error al aplicar el cupón: ' + (err.error?.error || 'Cupón inválido'));
          }
        });
      }
    } else {
      // Cupones genéricos disponibles para todos
      const validCoupons: { [key: string]: number } = {
        'BIENVENIDO10': 10,
        'DESCUENTO20': 20,
        'VERANO15': 15
      };
      
      const couponUpper = this.couponCode.toUpperCase();
      
      if (validCoupons[couponUpper]) {
        this.appliedCoupon = couponUpper;
        this.couponDiscount = validCoupons[couponUpper];
        this.calculateTotal();
        alert(`¡Cupón aplicado! Descuento de €${this.couponDiscount}`);
      } else {
        alert('Cupón inválido');
      }
    }
  }
  
  removeCoupon(): void {
    this.appliedCoupon = null;
    this.couponDiscount = 0;
    this.couponCode = '';
    this.calculateTotal();
  }

  proceedToCheckout(): void {
    if (!this.currentUser) {
      const message = `Subtotal: €${this.cartSubtotal.toFixed(2)}\nTotal: €${this.cartTotal.toFixed(2)}\n\n¡Regístrate para obtener un 10% de descuento en todas tus compras y cupones en cada compra!`;
      alert(message);
      this.clearCart();
    } else {
      // Procesar compra y generar cupón
      this.couponService.checkout(this.cartTotal, this.cartDiscount + this.couponDiscount, this.appliedCoupon).subscribe({
        next: (response) => {
          const message = `¡Compra realizada exitosamente!\n\nSubtotal: €${this.cartSubtotal.toFixed(2)}\nDescuento de usuario (10%): -€${this.cartDiscount.toFixed(2)}\n${this.appliedCoupon ? `Cupón ${this.appliedCoupon}: -€${this.couponDiscount.toFixed(2)}\n` : ''}Total pagado: €${this.cartTotal.toFixed(2)}\n\n🎁 ¡NUEVO CUPÓN GENERADO!\nCódigo: ${response.new_coupon.code}\nDescuento: €${response.new_coupon.amount}\n\n¡Úsalo en tu próxima compra!`;
          alert(message);
          this.clearCart();
          this.removeCoupon();
          this.loadUserCoupons(); // Recargar cupones
        },
        error: (err) => {
          alert('Error al procesar la compra: ' + (err.error?.error || 'Error desconocido'));
        }
      });
    }
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/home']);
  }

  goToUsers(): void {
    if (this.currentUser?.role === 'admin') {
      this.router.navigate(['/users']);
    }
  }
}
