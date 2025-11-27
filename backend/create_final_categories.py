import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def create_final_categories():
    """Crea subcategorías para las últimas 6 categorías"""
    
    categories_data = {
        'Libros': {
            'subcategories': [
                ('Ficción', 'Novelas y narrativa', 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400'),
                ('No Ficción', 'Ensayo y biografías', 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=400'),
                ('Infantil', 'Libros para niños', 'https://images.unsplash.com/photo-1516414447565-b14be0adf13e?w=400'),
                ('Cómics', 'Novelas gráficas y manga', 'https://images.unsplash.com/photo-1612178537253-bccd437b730e?w=400'),
                ('Educativos', 'Estudio y formación', 'https://images.unsplash.com/photo-1456513080510-7bf3a84b82f8?w=400'),
                ('Cocina', 'Recetas y gastronomía', 'https://images.unsplash.com/photo-1589998059171-988d887df646?w=400')
            ],
            'products': {
                'Ficción': [
                    ('Cien Años de Soledad', 'Gabriel García Márquez', 19.99, 30),
                    ('1984', 'George Orwell', 14.99, 40),
                    ('El Señor de los Anillos', 'J.R.R. Tolkien - Trilogía', 39.99, 25),
                    ('Harry Potter Saga Completa', 'J.K. Rowling', 89.99, 20),
                    ('Don Quijote de la Mancha', 'Miguel de Cervantes', 24.99, 35),
                    ('Orgullo y Prejuicio', 'Jane Austen', 16.99, 38)
                ],
                'No Ficción': [
                    ('Sapiens', 'Yuval Noah Harari', 22.99, 30),
                    ('Hábitos Atómicos', 'James Clear', 19.99, 35),
                    ('El Arte de la Guerra', 'Sun Tzu', 12.99, 45),
                    ('Steve Jobs Biografía', 'Walter Isaacson', 24.99, 25),
                    ('Pensar Rápido, Pensar Despacio', 'Daniel Kahneman', 21.99, 28),
                    ('El Poder del Ahora', 'Eckhart Tolle', 17.99, 32)
                ],
                'Infantil': [
                    ('El Principito', 'Antoine de Saint-Exupéry', 9.99, 50),
                    ('Harry Potter y la Piedra Filosofal', 'J.K. Rowling - Ilustrado', 24.99, 30),
                    ('Diario de Greg Colección', 'Jeff Kinney - 5 libros', 39.99, 25),
                    ('Cuentos de Buenas Noches', 'Colección ilustrada', 14.99, 40),
                    ('El Monstruo de Colores', 'Anna Llenas', 16.99, 35),
                    ('Colección Gerónimo Stilton', '10 libros', 49.99, 20)
                ],
                'Cómics': [
                    ('One Piece Vol. 1-3', 'Eiichiro Oda', 24.99, 30),
                    ('Batman: Año Uno', 'Frank Miller', 19.99, 25),
                    ('Naruto Box Set', 'Masashi Kishimoto', 149.00, 15),
                    ('Watchmen', 'Alan Moore', 29.99, 22),
                    ('Dragon Ball Edición Coleccionista', 'Akira Toriyama', 199.00, 12),
                    ('Maus', 'Art Spiegelman', 24.99, 28)
                ],
                'Educativos': [
                    ('Matemáticas para Bachillerato', 'Teoría y ejercicios', 34.99, 30),
                    ('Inglés Completo - Método Vaughan', 'Con audios', 44.99, 25),
                    ('Física y Química ESO', 'Editorial SM', 29.99, 35),
                    ('Historia del Mundo', 'Enciclopedia ilustrada', 39.99, 20),
                    ('Programación Python para Principiantes', 'Con ejercicios', 32.99, 28),
                    ('Atlas Mundial', 'Geografía actualizada', 24.99, 32)
                ],
                'Cocina': [
                    ('1080 Recetas de Cocina', 'Simone Ortega', 29.99, 30),
                    ('Cocina con Jamie Oliver', 'Jamie Oliver', 24.99, 25),
                    ('Repostería Fácil', 'Postres y tartas', 19.99, 35),
                    ('Cocina Vegana', 'Recetas saludables', 22.99, 28),
                    ('El Libro de la Cocina Española', 'Traditional recipes', 34.99, 22),
                    ('Batch Cooking', 'Organiza tu semana', 18.99, 32)
                ]
            }
        },
        'Juguetes': {
            'subcategories': [
                ('Bebés', 'Juguetes para bebés', 'https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=400'),
                ('Preescolar', 'Educativos 3-6 años', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400'),
                ('Construcción', 'LEGO y bloques', 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=400'),
                ('Muñecas', 'Muñecas y accesorios', 'https://images.unsplash.com/photo-1518562923427-c7d5e992a9f8?w=400'),
                ('Juegos de Mesa', 'Para toda la familia', 'https://images.unsplash.com/photo-1611891487781-f0f8e3659d94?w=400'),
                ('Electrónicos', 'Juguetes tech', 'https://images.unsplash.com/photo-1559911773-1cd6e2c1eb76?w=400')
            ],
            'products': {
                'Bebés': [
                    ('Gimnasio Actividades Bebé', 'Con música y luces', 49.99, 25),
                    ('Sonajeros Set 5', 'Colores y texturas', 19.99, 40),
                    ('Móvil Musical Cuna', 'Proyector estrellas', 34.99, 30),
                    ('Cubos Apilables', '10 piezas educativas', 16.99, 35),
                    ('Peluche Musical', 'Suave con melodías', 24.99, 32),
                    ('Juguete Baño Set', '8 piezas flotantes', 14.99, 45)
                ],
                'Preescolar': [
                    ('Puzzle Madera Animales', '4 puzzles 12 piezas', 22.99, 35),
                    ('Plastilina 24 Colores', 'No tóxica', 19.99, 40),
                    ('Bloques Construcción Grandes', '50 piezas colores', 29.99, 30),
                    ('Cocinita de Juguete', 'Con accesorios', 69.99, 20),
                    ('Pizarra Magnética Infantil', 'Doble cara con letras', 34.99, 28),
                    ('Tren de Madera', 'Con vías 30 piezas', 44.99, 25)
                ],
                'Construcción': [
                    ('LEGO Classic Caja Grande', '1000 piezas', 59.99, 30),
                    ('LEGO Star Wars Millennium Falcon', 'Edición coleccionista', 159.00, 15),
                    ('Bloques Magnéticos', '100 piezas 3D', 49.99, 25),
                    ('LEGO Technic Coche Deportivo', 'Con motor', 89.99, 20),
                    ('Construcción Arquitectura', 'Edificios famosos', 79.99, 18),
                    ('Set Bloques Madera', '200 piezas naturales', 39.99, 28)
                ],
                'Muñecas': [
                    ('Barbie Dreamhouse', 'Casa con accesorios', 199.00, 12),
                    ('Bebé Nenuco', 'Interactivo llora', 49.99, 25),
                    ('LOL Surprise Set', 'Colección 6 muñecas', 59.99, 30),
                    ('Casa de Muñecas Madera', '3 plantas amueblada', 129.00, 15),
                    ('Nancy Clásica', 'Con vestidos', 34.99, 28),
                    ('Carrito Bebé Muñecas', 'Plegable rosa', 39.99, 22)
                ],
                'Juegos de Mesa': [
                    ('Monopoly Edición España', 'Juego clásico', 29.99, 30),
                    ('Catán', 'Juego de estrategia', 39.99, 25),
                    ('Uno Cartas', 'Para toda la familia', 9.99, 50),
                    ('Scrabble Original', 'Juego de palabras', 24.99, 28),
                    ('Cluedo', 'Misterio detective', 27.99, 32),
                    ('Jenga Classic', 'Torre de madera', 19.99, 35)
                ],
                'Electrónicos': [
                    ('Robot Programable', 'STEM educativo', 79.99, 20),
                    ('Tablet Infantil', 'Android 7" control parental', 89.99, 25),
                    ('Dron Mini Kids', 'Fácil control', 49.99, 30),
                    ('Consola Portátil Retro', '400 juegos clásicos', 39.99, 35),
                    ('Reloj Inteligente Niños', 'GPS y llamadas', 59.99, 28),
                    ('Microscopio Digital Infantil', 'Con pantalla LCD', 69.99, 22)
                ]
            }
        },
        'Belleza y Cuidado Personal': {
            'subcategories': [
                ('Maquillaje', 'Cosméticos y make-up', 'https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400'),
                ('Cuidado de la Piel', 'Cremas y tratamientos', 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=400'),
                ('Perfumes', 'Fragancias y colonias', 'https://images.unsplash.com/photo-1541643600914-78b084683601?w=400'),
                ('Cabello', 'Productos capilares', 'https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=400'),
                ('Higiene Personal', 'Cuidado diario', 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400'),
                ('Cuidado Masculino', 'Grooming para hombre', 'https://images.unsplash.com/photo-1503919005314-30d93d07d823?w=400')
            ],
            'products': {
                'Maquillaje': [
                    ('Paleta Sombras Ojos', '35 colores profesional', 29.99, 30),
                    ('Base de Maquillaje', 'Larga duración 30ml', 24.99, 40),
                    ('Set Brochas Maquillaje', '12 piezas profesional', 34.99, 25),
                    ('Máscara de Pestañas', 'Efecto volumen', 16.99, 50),
                    ('Labial Mate Líquido', 'Set 6 colores', 39.99, 35),
                    ('Iluminador Facial', 'Polvo y cremoso', 22.99, 32)
                ],
                'Cuidado de la Piel': [
                    ('Crema Facial Antiarrugas', 'Ácido hialurónico', 34.99, 30),
                    ('Sérum Vitamina C', '30ml concentrado', 29.99, 35),
                    ('Limpiador Facial', 'Todo tipo de pieles', 16.99, 45),
                    ('Mascarilla Facial Set', '10 unidades hidratante', 19.99, 40),
                    ('Contorno de Ojos', 'Antiojeras 15ml', 24.99, 28),
                    ('Protector Solar SPF50', 'Facial 50ml', 19.99, 50)
                ],
                'Perfumes': [
                    ('Perfume Chanel N°5', 'Eau de Parfum 100ml', 129.00, 20),
                    ('Colonia Hombre', 'Fragancia intensa 100ml', 59.99, 25),
                    ('Set Miniaturas Perfumes', '5 fragancias mujer', 44.99, 30),
                    ('Agua de Colonia Fresca', 'Unisex 200ml', 34.99, 35),
                    ('Perfume Floral', 'Mujer elegante 50ml', 79.99, 22),
                    ('Body Splash', 'Fragancia ligera 250ml', 19.99, 40)
                ],
                'Cabello': [
                    ('Champú y Acondicionador', 'Reparador 2x400ml', 24.99, 35),
                    ('Mascarilla Capilar', 'Hidratación intensa', 16.99, 40),
                    ('Aceite Argán', 'Para cabello 100ml', 19.99, 30),
                    ('Secador Profesional', '2200W con difusor', 49.99, 25),
                    ('Plancha de Pelo', 'Cerámica regulable', 39.99, 28),
                    ('Cepillo Desenredante', 'Efecto masaje', 12.99, 50)
                ],
                'Higiene Personal': [
                    ('Gel de Ducha Pack 3', '750ml hidratante', 14.99, 50),
                    ('Desodorante Roll-on', 'Pack 4 sin alcohol', 12.99, 60),
                    ('Cepillo Eléctrico Dental', 'Recargable con temporizador', 59.99, 25),
                    ('Jabón Natural Artesanal', 'Set 6 unidades', 19.99, 40),
                    ('Esponja Exfoliante Corporal', 'Pack 3 colores', 9.99, 55),
                    ('Crema de Manos', 'Pack 5 tubos 30ml', 16.99, 45)
                ],
                'Cuidado Masculino': [
                    ('Kit Afeitado Clásico', 'Navaja, brocha y jabón', 49.99, 25),
                    ('Maquinilla Eléctrica', 'Afeitado en seco y húmedo', 89.99, 20),
                    ('Bálsamo After Shave', 'Calmante 100ml', 19.99, 35),
                    ('Recortadora de Barba', 'Precisión profesional', 44.99, 28),
                    ('Aceite para Barba', 'Hidratante 50ml', 24.99, 32),
                    ('Set Cuidado Facial Hombre', 'Limpiador e hidratante', 34.99, 30)
                ]
            }
        },
        'Automóvil': {
            'subcategories': [
                ('Accesorios Interior', 'Complementos interiores', 'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=400'),
                ('Herramientas', 'Herramientas mecánicas', 'https://images.unsplash.com/photo-1530124566582-a618bc2615dc?w=400'),
                ('Limpieza', 'Productos de limpieza', 'https://images.unsplash.com/photo-1601362840469-51e4d8d58785?w=400'),
                ('Repuestos', 'Piezas de recambio', 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400'),
                ('Electrónica Auto', 'Gadgets tecnológicos', 'https://images.unsplash.com/photo-1617469767053-d3b523a0b982?w=400'),
                ('Aceites y Fluidos', 'Mantenimiento motor', 'https://images.unsplash.com/photo-1486262715619-67b85e0b08d3?w=400')
            ],
            'products': {
                'Accesorios Interior': [
                    ('Alfombrillas Universales', 'Goma 4 piezas', 29.99, 40),
                    ('Organizador Maletero', 'Plegable compartimentos', 24.99, 35),
                    ('Soporte Móvil Coche', 'Rejilla ventilación', 14.99, 60),
                    ('Ambientador Coche Set', '6 fragancias', 12.99, 50),
                    ('Funda Asientos Universales', 'Textil transpirable', 49.99, 25),
                    ('Cargador USB Dual', 'Carga rápida 3.0', 19.99, 45)
                ],
                'Herramientas': [
                    ('Maletín Herramientas', '150 piezas completo', 89.99, 20),
                    ('Gato Hidráulico', '2 toneladas portátil', 49.99, 25),
                    ('Compresor Aire Portátil', '12V digital', 39.99, 30),
                    ('Cables Arranque Batería', '3 metros reforzados', 24.99, 35),
                    ('Llave Impacto Eléctrica', 'Inalámbrica 18V', 129.00, 15),
                    ('Kit Reparación Pinchazos', 'Portátil completo', 19.99, 40)
                ],
                'Limpieza': [
                    ('Kit Lavado Coche', 'Shampoo, esponja y microfibra', 29.99, 40),
                    ('Aspiradora Coche 12V', 'Potente portátil', 34.99, 30),
                    ('Cera Carnauba', 'Protección brillo 300ml', 19.99, 35),
                    ('Limpiador Interior', 'Spray multiusos 500ml', 12.99, 50),
                    ('Paños Microfibra Pack', '10 unidades premium', 16.99, 45),
                    ('Pulidora Orbital', 'Eléctrica 700W', 79.99, 20)
                ],
                'Repuestos': [
                    ('Escobillas Limpiaparabrisas', 'Universal 55cm par', 19.99, 40),
                    ('Filtro Aire Motor', 'Alta eficiencia', 14.99, 35),
                    ('Bombillas H7 Halógenas', 'Pack 2 larga duración', 24.99, 50),
                    ('Pastillas Freno Delanteras', 'Cerámica', 49.99, 25),
                    ('Filtro Habitáculo', 'Carbón activo', 16.99, 45),
                    ('Bujías Iridio Set 4', 'Alto rendimiento', 39.99, 30)
                ],
                'Electrónica Auto': [
                    ('Cámara Retrovisor Parking', 'Visión nocturna', 49.99, 30),
                    ('Dashcam Full HD', 'Grabación continua', 79.99, 25),
                    ('GPS Navegador', 'Pantalla 7" mapas Europa', 99.99, 20),
                    ('Sensor Aparcamiento', 'Kit 4 sensores display', 39.99, 35),
                    ('Transmisor FM Bluetooth', 'Manos libres USB', 19.99, 45),
                    ('Alarma Antirrobo', 'Con mando', 59.99, 28)
                ],
                'Aceites y Fluidos': [
                    ('Aceite Motor 5W30', 'Sintético 5 litros', 39.99, 30),
                    ('Líquido Anticongelante', 'Refrigerante 5L', 24.99, 35),
                    ('Líquido Frenos DOT4', '1 litro', 12.99, 40),
                    ('Aditivo Limpiador Inyectores', '300ml gasolina', 16.99, 38),
                    ('Líquido Limpiaparabrisas', 'Concentrado 5L', 9.99, 50),
                    ('Aceite Transmisión ATF', 'Automático 1L', 19.99, 32)
                ]
            }
        },
        'Jardín': {
            'subcategories': [
                ('Plantas y Semillas', 'Flora para jardín', 'https://images.unsplash.com/photo-1466692476868-aef1dfb1e735?w=400'),
                ('Herramientas Jardín', 'Equipamiento jardinería', 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400'),
                ('Mobiliario Exterior', 'Muebles de jardín', 'https://images.unsplash.com/photo-1600210491892-03d54c0aaf87?w=400'),
                ('Barbacoas', 'BBQ y parrillas', 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1?w=400'),
                ('Decoración Jardín', 'Ornamentos exteriores', 'https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=400'),
                ('Riego', 'Sistemas de riego', 'https://images.unsplash.com/photo-1563514227147-6d2ff665a6a0?w=400')
            ],
            'products': {
                'Plantas y Semillas': [
                    ('Set Semillas Huerto', '12 variedades verduras', 19.99, 40),
                    ('Plantas Aromáticas Set 6', 'Macetas incluidas', 29.99, 30),
                    ('Semillas Flores Colores', 'Mix primavera', 14.99, 50),
                    ('Abono Universal', 'Granulado 5kg', 16.99, 35),
                    ('Sustrato Plantas', 'Ecológico 20L', 12.99, 45),
                    ('Bulbos Tulipanes', 'Pack 50 colores variados', 24.99, 28)
                ],
                'Herramientas Jardín': [
                    ('Cortacésped Eléctrico', '1600W 38cm', 159.00, 15),
                    ('Desbrozadora Gasolina', '52cc 2 tiempos', 199.00, 12),
                    ('Set Herramientas Jardín', '5 piezas acero inoxidable', 49.99, 30),
                    ('Tijeras Podar Eléctricas', 'Batería litio', 89.99, 20),
                    ('Soplador Hojas', 'Eléctrico 3000W', 79.99, 22),
                    ('Carretilla Jardín', '60L metálica', 59.99, 25)
                ],
                'Mobiliario Exterior': [
                    ('Conjunto Mesa y 4 Sillas', 'Ratán sintético', 299.00, 15),
                    ('Tumbona Plegable', 'Aluminio regulable', 79.99, 25),
                    ('Sombrilla Jardín 3m', 'Con base incluida', 129.00, 18),
                    ('Banco Madera Exterior', '120cm tratado', 89.99, 20),
                    ('Hamaca Jardin Doble', 'Con soporte 200kg', 149.00, 15),
                    ('Cojines Exterior Set 4', 'Impermeables', 39.99, 35)
                ],
                'Barbacoas': [
                    ('Barbacoa Gas 3 Quemadores', 'Con tapa y termómetro', 399.00, 12),
                    ('Barbacoa Carbón Weber', 'Clásica 57cm', 249.00, 15),
                    ('Barbacoa Eléctrica', 'Sin humo 2000W', 129.00, 20),
                    ('Set Utensilios BBQ', '18 piezas acero inoxidable', 44.99, 30),
                    ('Carbón Vegetal', 'Premium 10kg', 19.99, 50),
                    ('Funda Protectora BBQ', 'Impermeable universal', 29.99, 35)
                ],
                'Decoración Jardín': [
                    ('Luces Solares Jardín', 'Pack 8 LED', 34.99, 40),
                    ('Fuente Agua Decorativa', 'Con bomba solar', 89.99, 20),
                    ('Maceteros Decorativos', 'Set 3 tamaños resina', 49.99, 30),
                    ('Enano Jardín Figura', 'Decoración resina 30cm', 24.99, 35),
                    ('Tira Luces LED Exterior', '10m RGB impermeable', 29.99, 45),
                    ('Arco Jardin Metal', 'Para plantas trepadoras', 69.99, 22)
                ],
                'Riego': [
                    ('Manguera Jardín 30m', 'Extensible no se enreda', 39.99, 35),
                    ('Sistema Riego Automático', 'Programador + goteo', 89.99, 25),
                    ('Aspersor Giratorio', 'Ajustable 360°', 19.99, 40),
                    ('Kit Goteo 50m', 'Para 50 plantas', 49.99, 30),
                    ('Pistola Riego 8 Funciones', 'Metal resistente', 24.99, 38),
                    ('Depósito Agua Lluvia', '300L con grifo', 79.99, 18)
                ]
            }
        },
        'Oficina': {
            'subcategories': [
                ('Papelería', 'Material de escritura', 'https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=400'),
                ('Tecnología Oficina', 'Equipamiento tech', 'https://images.unsplash.com/photo-1531297484001-80022131f5a1?w=400'),
                ('Organización', 'Archivadores y organizadores', 'https://images.unsplash.com/photo-1544120596-6a40e8e0d222?w=400'),
                ('Muebles Oficina', 'Mobiliario workspace', 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=400'),
                ('Impresión', 'Tintas y consumibles', 'https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400'),
                ('Presentación', 'Material para presentar', 'https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=400')
            ],
            'products': {
                'Papelería': [
                    ('Bolígrafos BIC Pack 50', 'Azul tinta fluida', 12.99, 60),
                    ('Cuadernos A4 Pack 5', 'Tapa dura 100 hojas', 19.99, 45),
                    ('Post-it Notes Colores', 'Pack 12 blocs', 16.99, 50),
                    ('Set Marcadores Fluorescentes', '36 colores', 24.99, 35),
                    ('Papel Folios A4', 'Pack 5 paquetes 500 hojas', 29.99, 40),
                    ('Grapadora Profesional', 'Hasta 60 hojas', 19.99, 38)
                ],
                'Tecnología Oficina': [
                    ('Impresora Multifunción HP', 'WiFi color escáner', 149.00, 20),
                    ('Calculadora Científica', 'Casio programable', 34.99, 30),
                    ('Destructora Documentos', 'Corte cruzado', 79.99, 18),
                    ('Teléfono Fijo Inalámbrico', 'Duo con contestador', 59.99, 25),
                    ('Scanner Portátil', 'Documentos A4 USB', 89.99, 22),
                    ('Webcam Full HD', 'Con micrófono 1080p', 44.99, 35)
                ],
                'Organización': [
                    ('Archivadores Pack 10', 'Cartón A4 lomo ancho', 24.99, 40),
                    ('Organizador Escritorio', 'Bambú compartimentos', 29.99, 35),
                    ('Cajonera Oficina', '5 cajones ruedas', 49.99, 25),
                    ('Carpetas Colgantes Pack 25', 'Con pestañas', 19.99, 45),
                    ('Bandeja Documentos 3 Niveles', 'Apilable metal negro', 34.99, 30),
                    ('Tablón Corcho', '90x60cm con marco', 24.99, 32)
                ],
                'Muebles Oficina': [
                    ('Silla Ergonómica Oficina', 'Con reposabrazos', 149.00, 20),
                    ('Escritorio Regulable Altura', 'Eléctrico 120x60cm', 399.00, 12),
                    ('Estantería Oficina', '5 baldas metálica', 89.99, 18),
                    ('Mesa Reuniones', '180x90cm para 6 personas', 299.00, 10),
                    ('Reposapiés Ajustable', 'Ergonómico', 29.99, 35),
                    ('Lámpara Escritorio LED', 'Regulable táctil', 39.99, 30)
                ],
                'Impresión': [
                    ('Cartuchos Tinta HP Pack', 'Negro y color', 49.99, 35),
                    ('Tóner Láser Compatible', 'Negro alto rendimiento', 39.99, 30),
                    ('Papel Foto Brillante', 'A4 100 hojas 200gr', 19.99, 40),
                    ('Etiquetas Adhesivas', '1000 unidades blancas', 14.99, 45),
                    ('Plastificadora A4', 'Con 100 fundas', 44.99, 25),
                    ('Fundas Plástico A4', 'Pack 100 multitaladro', 9.99, 60)
                ],
                'Presentación': [
                    ('Pizarra Blanca Magnética', '90x60cm con accesorios', 49.99, 25),
                    ('Rotuladores Pizarra Pack 12', 'Colores borrables', 16.99, 40),
                    ('Puntero Láser Presentación', 'Con mando diapositivas', 24.99, 32),
                    ('Portapóster Enrollable', '120x200cm retráctil', 39.99, 28),
                    ('Carpetas Presentación', 'Pack 10 fundas 40 hojas', 29.99, 35),
                    ('Atril Documentos', 'Regulable metal', 34.99, 30)
                ]
            }
        }
    }
    
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD', ''),
            database=os.getenv('DB_NAME', 'tiendas_online'),
            port=int(os.getenv('DB_PORT', 3306)),
            cursorclass=pymysql.cursors.DictCursor
        )
        
        cursor = connection.cursor()
        
        print("="*60)
        print("CREANDO CATEGORÍAS FINALES")
        print("="*60)
        
        total_subcats = 0
        total_products = 0
        
        for cat_name, cat_data in categories_data.items():
            cursor.execute("SELECT id FROM categories WHERE name = %s AND parent_id IS NULL", (cat_name,))
            category = cursor.fetchone()
            
            if not category:
                print(f"\n⚠️ Categoría {cat_name} no encontrada")
                continue
            
            cat_id = category['id']
            print(f"\n{cat_name} (ID: {cat_id})")
            
            # Crear subcategorías
            subcat_ids = {}
            for subcat_name, subcat_desc, subcat_img in cat_data['subcategories']:
                cursor.execute("""
                    INSERT INTO categories (name, description, image_url, parent_id) 
                    VALUES (%s, %s, %s, %s)
                """, (subcat_name, subcat_desc, subcat_img, cat_id))
                subcat_ids[subcat_name] = cursor.lastrowid
                total_subcats += 1
            
            connection.commit()
            
            # Insertar productos
            for subcat_name, products in cat_data['products'].items():
                # Usar la primera imagen de la subcategoría como base
                base_img = next((img for name, desc, img in cat_data['subcategories'] if name == subcat_name), 
                               'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400')
                
                for prod_name, prod_desc, price, stock in products:
                    cursor.execute("""
                        INSERT INTO products (name, description, price, stock, image_url, category_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (prod_name, prod_desc, price, stock, base_img, subcat_ids[subcat_name]))
                    total_products += 1
                print(f"  ✓ {subcat_name}: {len(products)} productos")
            
            connection.commit()
        
        print(f"\n{'='*60}")
        print(f"✅ Categorías finales completadas")
        print(f"Subcategorías: {total_subcats} | Productos: {total_products}")
        print(f"{'='*60}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_final_categories()
