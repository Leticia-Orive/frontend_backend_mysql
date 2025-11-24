import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../services/user.service';
import { User } from '../../models/user.model';

@Component({
  selector: 'app-user-list',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './user-list.component.html',
  styleUrl: './user-list.component.css'
})
export class UserListComponent implements OnInit {
  users: User[] = [];
  loading = false;
  error: string | null = null;
  
  // Form data
  showForm = false;
  isEditing = false;
  currentUser: Partial<User> = {
    name: '',
    email: ''
  };

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.loadUsers();
  }

  loadUsers(): void {
    this.loading = true;
    this.error = null;
    this.userService.getUsers().subscribe({
      next: (data) => {
        this.users = data;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Error al cargar usuarios: ' + (err.error?.error || err.message);
        this.loading = false;
      }
    });
  }

  openCreateForm(): void {
    this.showForm = true;
    this.isEditing = false;
    this.currentUser = { name: '', email: '' };
  }

  openEditForm(user: User): void {
    this.showForm = true;
    this.isEditing = true;
    this.currentUser = { ...user };
  }

  closeForm(): void {
    this.showForm = false;
    this.currentUser = { name: '', email: '' };
  }

  saveUser(): void {
    if (!this.currentUser.name || !this.currentUser.email) {
      alert('Por favor completa todos los campos');
      return;
    }

    if (this.isEditing && this.currentUser.id) {
      this.userService.updateUser(this.currentUser.id, this.currentUser).subscribe({
        next: () => {
          this.loadUsers();
          this.closeForm();
        },
        error: (err) => {
          this.error = 'Error al actualizar usuario: ' + (err.error?.error || err.message);
        }
      });
    } else {
      this.userService.createUser(this.currentUser).subscribe({
        next: () => {
          this.loadUsers();
          this.closeForm();
        },
        error: (err) => {
          this.error = 'Error al crear usuario: ' + (err.error?.error || err.message);
        }
      });
    }
  }

  deleteUser(id: number): void {
    if (confirm('¿Estás seguro de que quieres eliminar este usuario?')) {
      this.userService.deleteUser(id).subscribe({
        next: () => {
          this.loadUsers();
        },
        error: (err) => {
          this.error = 'Error al eliminar usuario: ' + (err.error?.error || err.message);
        }
      });
    }
  }
}
