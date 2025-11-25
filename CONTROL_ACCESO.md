# Control de Acceso por Roles - Documentación

## Resumen de Cambios

Se ha implementado un sistema de control de acceso basado en roles para que:
- ✅ Los **administradores** puedan ver y gestionar todos los usuarios
- ❌ Los **usuarios normales** NO puedan acceder a la lista de usuarios

## Cambios Implementados

### Backend (Python/Flask)

1. **Nuevo Decorator `admin_required`** (`backend/app.py`)
   - Verifica que el token JWT contenga el rol de 'admin'
   - Retorna error 403 si el usuario no es administrador
   - Valida automáticamente la autenticación

2. **Endpoint `/api/users` actualizado**
   - Ahora requiere rol de administrador (usa `@admin_required`)
   - Incluye el campo `role` en la respuesta
   - Retorna error 403 para usuarios no autorizados

### Frontend (Angular)

1. **Nuevo Guard `adminGuard`** (`frontend/src/app/guards/auth.guard.ts`)
   - Verifica que el usuario esté autenticado
   - Verifica que el usuario tenga rol 'admin'
   - Redirige a `/home` si no es administrador
   - Muestra alerta informativa

2. **Nuevo Componente `HomeComponent`**
   - Página principal para todos los usuarios autenticados
   - Muestra información del usuario actual
   - Botón "Ver Usuarios" solo visible para administradores
   - Botón de cerrar sesión

3. **Rutas Actualizadas** (`frontend/src/app/app.routes.ts`)
   ```typescript
   /home    - Página principal (requiere autenticación)
   /users   - Gestión de usuarios (requiere rol admin)
   /login   - Inicio de sesión
   /register - Registro
   ```

4. **Componente UserList Actualizado**
   - Botones de navegación (Inicio, Cerrar Sesión)
   - Muestra el rol de cada usuario en la tabla
   - Badges visuales para distinguir roles

## Cómo Probar

### 1. Crear un Usuario Administrador
```bash
# El usuario debe registrarse con rol "Administrador" en el formulario
```

### 2. Crear un Usuario Normal
```bash
# El usuario debe registrarse con rol "Usuario" en el formulario
```

### 3. Probar como Administrador
1. Inicia sesión con el usuario administrador
2. Serás redirigido a `/home`
3. Verás el botón "👥 Ver Usuarios"
4. Haz clic y podrás acceder a la gestión de usuarios
5. Verás todos los usuarios con sus roles

### 4. Probar como Usuario Normal
1. Inicia sesión con el usuario normal
2. Serás redirigido a `/home`
3. NO verás el botón "Ver Usuarios"
4. Verás un mensaje informativo sobre las restricciones
5. Si intentas acceder manualmente a `/users`, serás bloqueado y redirigido

## Códigos de Respuesta HTTP

- **200 OK**: Operación exitosa
- **401 Unauthorized**: Token no proporcionado o inválido
- **403 Forbidden**: Usuario no tiene permisos de administrador
- **404 Not Found**: Recurso no encontrado

## Estructura de Tokens JWT

Los tokens ahora incluyen:
```json
{
  "user_id": 1,
  "role": "admin" | "user",
  "exp": "timestamp"
}
```

## Seguridad

- ✅ Validación en Backend (no se puede eludir)
- ✅ Validación en Frontend (mejor experiencia de usuario)
- ✅ Tokens JWT con información de roles
- ✅ Decorators específicos por nivel de acceso
- ✅ Mensajes claros de error

## Próximos Pasos Sugeridos

1. Agregar más roles (moderador, editor, etc.)
2. Implementar permisos granulares por recurso
3. Agregar logs de auditoría para acciones administrativas
4. Implementar renovación automática de tokens
5. Agregar página de perfil de usuario
