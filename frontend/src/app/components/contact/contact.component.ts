import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../services/auth.service';

interface ContactMessage {
  name: string;
  email: string;
  phone: string;
  subject: string;
  message: string;
}

@Component({
  selector: 'app-contact',
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './contact.component.html',
  styleUrl: './contact.component.css'
})
export class ContactComponent implements OnInit {
  currentUser: any = null;
  
  contactForm: ContactMessage = {
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  };

  subjects = [
    'Consulta sobre productos',
    'Problema con mi pedido',
    'Devoluciones y reembolsos',
    'Problemas técnicos',
    'Sugerencias',
    'Quejas',
    'Otros'
  ];

  showSuccessMessage = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.authService.currentUser$.subscribe(user => {
      this.currentUser = user;
      if (user) {
        // Pre-rellenar datos del usuario si está logueado
        this.contactForm.name = user.name || '';
        this.contactForm.email = user.email || '';
      }
    });
  }

  submitForm(): void {
    // Validar campos requeridos
    if (!this.contactForm.name || !this.contactForm.email || !this.contactForm.subject || !this.contactForm.message) {
      alert('Por favor completa todos los campos obligatorios');
      return;
    }

    // Validar email
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(this.contactForm.email)) {
      alert('Por favor ingresa un email válido');
      return;
    }

    // Aquí normalmente enviarías los datos al backend
    console.log('Formulario de contacto enviado:', this.contactForm);

    // Mostrar mensaje de éxito
    this.showSuccessMessage = true;

    // Limpiar formulario después de 3 segundos
    setTimeout(() => {
      this.resetForm();
      this.showSuccessMessage = false;
    }, 3000);
  }

  resetForm(): void {
    if (!this.currentUser) {
      this.contactForm = {
        name: '',
        email: '',
        phone: '',
        subject: '',
        message: ''
      };
    } else {
      // Mantener nombre y email del usuario
      this.contactForm = {
        name: this.currentUser.name || '',
        email: this.currentUser.email || '',
        phone: '',
        subject: '',
        message: ''
      };
    }
  }

  goBack(): void {
    this.router.navigate(['/home']);
  }
}
