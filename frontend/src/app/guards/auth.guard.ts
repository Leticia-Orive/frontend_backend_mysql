import { inject } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../services/auth.service';
import { map, take } from 'rxjs/operators';

export const authGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.isLoggedIn()) {
    return true;
  }

  router.navigate(['/login']);
  return false;
};

export const adminGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  // Primero verificar si está autenticado
  if (!authService.isLoggedIn()) {
    router.navigate(['/login']);
    return false;
  }

  // Esperar a que se cargue el usuario actual
  return authService.currentUser$.pipe(
    take(1),
    map(currentUser => {
      // Si no hay usuario después de esperar, redirigir a login
      if (!currentUser) {
        router.navigate(['/login']);
        return false;
      }

      // Verificar si es admin
      if (currentUser.role === 'admin') {
        return true;
      }

      // Si no es admin, mostrar alerta y redirigir a home
      alert('Acceso denegado. Solo los administradores pueden acceder a esta página.');
      router.navigate(['/home']);
      return false;
    })
  );
};

export const loginGuard = () => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (!authService.isLoggedIn()) {
    return true;
  }

  router.navigate(['/home']);
  return false;
};
