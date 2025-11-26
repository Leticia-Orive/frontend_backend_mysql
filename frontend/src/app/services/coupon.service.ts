import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CouponService {
  private apiUrl = 'http://127.0.0.1:5000/api';

  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const token = localStorage.getItem('token');
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`
    });
  }

  // Obtener cupones del usuario actual
  getMyCoupons(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/my-coupons`, {
      headers: this.getAuthHeaders()
    });
  }

  // Usar un cupón
  useCoupon(couponCode: string): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/use-coupon`, 
      { coupon_code: couponCode },
      { headers: this.getAuthHeaders() }
    );
  }

  // Procesar checkout y generar nuevo cupón
  checkout(totalAmount: number, discountApplied: number, couponUsed: string | null): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/checkout`, 
      { 
        total_amount: totalAmount,
        discount_applied: discountApplied,
        coupon_used: couponUsed
      },
      { headers: this.getAuthHeaders() }
    );
  }
}
