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
  appliedCoupons: Array<{code: string, amount: number}> = [];
  totalCouponDiscount = 0;
  userCoupons: any[] = [];
  showCouponsNotification = false;
  
  // Payment and pickup
  showPaymentModal = false;
  paymentMethod: 'tarjeta' | 'paypal' | 'bizum' | 'efectivo' | null = null;
  pickupPoint = '';
  showPickupOptions = false;
  pickupPoints = [
    'Tienda Madrid - Calle Gran Vía 28',
    'Tienda Barcelona - Plaza Catalunya 10',
    'Tienda Valencia - Calle Colón 45',
    'Tienda Sevilla - Avenida Constitución 15'
  ];
  
  // Card payment details
  showCardModal = false;
  cardNumber = '';
  cardHolder = '';
  cardExpiry = '';
  cardCVV = '';
  
  // Bizum payment details
  showBizumModal = false;
  bizumPhone = '';
  
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
    
    // Apply multiple coupon discounts
    this.totalCouponDiscount = this.appliedCoupons.reduce((sum, coupon) => sum + coupon.amount, 0);
    
    this.cartTotal = this.cartSubtotal - this.cartDiscount - this.totalCouponDiscount;
    
    // Ensure total doesn't go negative
    if (this.cartTotal < 0) {
      this.cartTotal = 0;
    }
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

  applyUserCoupon(couponCode: string): void {
    this.couponCode = couponCode;
    this.applyCoupon();
  }

  applyCoupon(): void {
    if (!this.couponCode.trim()) {
      alert('Por favor ingresa un código de cupón');
      return;
    }

    // Check if coupon is already applied
    if (this.appliedCoupons.some(c => c.code === this.couponCode.trim())) {
      alert('Este cupón ya está aplicado');
      return;
    }

    // Buscar el cupón en los cupones del usuario
    const userCoupon = this.userCoupons.find(c => c.coupon_code === this.couponCode.trim());
    
    if (userCoupon) {
      if (this.currentUser) {
        // Usuario registrado usando su cupón personal
        this.couponService.useCoupon(this.couponCode).subscribe({
          next: (response) => {
            this.appliedCoupons.push({
              code: this.couponCode,
              amount: response.discount_amount
            });
            this.calculateTotal();
            this.loadUserCoupons(); // Recargar cupones
            this.couponCode = '';
            alert(`¡Cupón aplicado! Descuento de €${response.discount_amount}`);
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
        this.appliedCoupons.push({
          code: couponUpper,
          amount: validCoupons[couponUpper]
        });
        this.calculateTotal();
        this.couponCode = '';
        alert(`¡Cupón aplicado! Descuento de €${validCoupons[couponUpper]}`);
      } else {
        alert('Cupón inválido');
      }
    }
  }
  
  removeCoupon(couponCode: string): void {
    this.appliedCoupons = this.appliedCoupons.filter(c => c.code !== couponCode);
    this.calculateTotal();
  }
  
  removeAllCoupons(): void {
    this.appliedCoupons = [];
    this.couponCode = '';
    this.calculateTotal();
  }

  proceedToCheckout(): void {
    if (this.cart.length === 0) {
      alert('El carrito está vacío');
      return;
    }
    
    // Cerrar el carrito y abrir modal de pago
    this.showCart = false;
    this.showPaymentModal = true;
    this.paymentMethod = null;
    this.pickupPoint = '';
    this.showPickupOptions = false;
  }
  
  selectPaymentMethod(method: 'tarjeta' | 'paypal' | 'bizum' | 'efectivo'): void {
    this.paymentMethod = method;
    
    // Solo efectivo requiere punto de recogida obligatorio
    if (method === 'efectivo') {
      this.showPickupOptions = true;
    } else {
      this.showPickupOptions = false;
      this.pickupPoint = '';
    }
  }
  
  confirmPayment(): void {
    if (!this.paymentMethod) {
      alert('Por favor selecciona un método de pago');
      return;
    }
    
    if (this.paymentMethod === 'efectivo' && !this.pickupPoint) {
      alert('Por favor selecciona un punto de recogida para pago en efectivo');
      return;
    }
    
    // Abrir modales específicos según el método de pago
    if (this.paymentMethod === 'tarjeta') {
      this.openCardModal();
      return;
    }
    
    if (this.paymentMethod === 'bizum') {
      this.openBizumModal();
      return;
    }
    
    // Para PayPal y Efectivo procesar directamente
    this.finalizePayment();
  }
  
  openCardModal(): void {
    this.showCardModal = true;
    this.cardNumber = '';
    this.cardHolder = '';
    this.cardExpiry = '';
    this.cardCVV = '';
  }
  
  closeCardModal(): void {
    this.showCardModal = false;
  }
  
  confirmCardPayment(): void {
    if (!this.cardNumber || !this.cardHolder || !this.cardExpiry || !this.cardCVV) {
      alert('Por favor completa todos los campos de la tarjeta');
      return;
    }
    
    if (this.cardNumber.length !== 16) {
      alert('El número de tarjeta debe tener 16 dígitos');
      return;
    }
    
    if (this.cardCVV.length !== 3) {
      alert('El CVV debe tener 3 dígitos');
      return;
    }
    
    this.closeCardModal();
    this.finalizePayment();
  }
  
  openBizumModal(): void {
    this.showBizumModal = true;
    this.bizumPhone = '';
  }
  
  closeBizumModal(): void {
    this.showBizumModal = false;
  }
  
  confirmBizumPayment(): void {
    if (!this.bizumPhone) {
      alert('Por favor ingresa tu número de teléfono');
      return;
    }
    
    if (this.bizumPhone.length !== 9) {
      alert('El número de teléfono debe tener 9 dígitos');
      return;
    }
    
    this.closeBizumModal();
    this.finalizePayment();
  }
  
  finalizePayment(): void {
    // Procesar según si está registrado o no
    if (!this.currentUser) {
      this.processGuestCheckout();
    } else {
      this.processUserCheckout();
    }
  }
  
  formatCardNumber(event: any): void {
    let value = event.target.value.replace(/\s/g, '');
    value = value.replace(/\D/g, '');
    if (value.length > 16) value = value.substr(0, 16);
    this.cardNumber = value;
  }
  
  formatExpiry(event: any): void {
    let value = event.target.value.replace(/\s/g, '');
    value = value.replace(/\D/g, '');
    if (value.length >= 2) {
      value = value.substr(0, 2) + '/' + value.substr(2, 2);
    }
    if (value.length > 5) value = value.substr(0, 5);
    this.cardExpiry = value;
  }
  
  formatCVV(event: any): void {
    let value = event.target.value.replace(/\D/g, '');
    if (value.length > 3) value = value.substr(0, 3);
    this.cardCVV = value;
  }
  
  formatPhone(event: any): void {
    let value = event.target.value.replace(/\D/g, '');
    if (value.length > 9) value = value.substr(0, 9);
    this.bizumPhone = value;
  }
  
  processGuestCheckout(): void {
    const pickupInfo = this.paymentMethod === 'efectivo' ? `\nPunto de recogida: ${this.pickupPoint}` : '';
    const message = `¡Pedido confirmado!\n\nMétodo de pago: ${this.getPaymentMethodName()}\nSubtotal: €${this.cartSubtotal.toFixed(2)}\nTotal: €${this.cartTotal.toFixed(2)}${pickupInfo}\n\n¡Regístrate para obtener un 10% de descuento y cupones en cada compra!`;
    alert(message);
    this.clearCart();
    this.closePaymentModal();
  }
  
  processUserCheckout(): void {
    // Procesar compra y generar cupón
    const couponsUsed = this.appliedCoupons.map(c => c.code).join(', ');
    this.couponService.checkout(this.cartTotal, this.cartDiscount + this.totalCouponDiscount, couponsUsed || null).subscribe({
      next: (response) => {
        const pickupInfo = this.paymentMethod === 'efectivo' ? `\nPunto de recogida: ${this.pickupPoint}` : '';
        const couponsInfo = this.appliedCoupons.length > 0 ? `Cupones aplicados: ${this.appliedCoupons.map(c => `${c.code} (-€${c.amount})`).join(', ')}\n` : '';
        const message = `¡Compra realizada exitosamente!\n\nMétodo de pago: ${this.getPaymentMethodName()}\nSubtotal: €${this.cartSubtotal.toFixed(2)}\nDescuento de usuario (10%): -€${this.cartDiscount.toFixed(2)}\n${couponsInfo}Total pagado: €${this.cartTotal.toFixed(2)}${pickupInfo}\n\n🎁 ¡NUEVO CUPÓN GENERADO!\nCódigo: ${response.new_coupon.code}\nDescuento: €${response.new_coupon.amount}\n\n¡Úsalo en tu próxima compra!`;
        alert(message);
        this.clearCart();
        this.removeAllCoupons();
        this.loadUserCoupons();
        this.closePaymentModal();
      },
      error: (err) => {
        alert('Error al procesar la compra: ' + (err.error?.error || 'Error desconocido'));
      }
    });
  }
  
  getPaymentMethodName(): string {
    const methods = {
      'tarjeta': 'Tarjeta de Crédito/Débito',
      'paypal': 'PayPal',
      'bizum': 'Bizum',
      'efectivo': 'Efectivo en Tienda'
    };
    return this.paymentMethod ? methods[this.paymentMethod] : '';
  }
  
  closePaymentModal(): void {
    this.showPaymentModal = false;
    this.paymentMethod = null;
    this.pickupPoint = '';
    this.showPickupOptions = false;
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
