import requests
import json

BASE_URL = 'http://localhost:5000/api'

def test_endpoints():
    """Prueba los endpoints de categorías y subcategorías"""
    
    print("=" * 70)
    print("PROBANDO ENDPOINTS DE CATEGORÍAS Y SUBCATEGORÍAS")
    print("=" * 70)
    
    # Test 1: Obtener todas las categorías principales
    print("\n1. GET /api/categories (sin subcategorías)")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/categories")
        if response.status_code == 200:
            categories = response.json()
            print(f"✓ Total de categorías principales: {len(categories)}")
            for cat in categories:
                print(f"  - {cat['name']} (ID: {cat['id']})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 2: Obtener todas las categorías con subcategorías
    print("\n2. GET /api/categories?include_subcategories=true")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/categories?include_subcategories=true")
        if response.status_code == 200:
            categories = response.json()
            print(f"✓ Total de categorías principales: {len(categories)}")
            for cat in categories:
                subcats = cat.get('subcategories', [])
                print(f"  - {cat['name']} (ID: {cat['id']}) - {len(subcats)} subcategorías")
                for subcat in subcats:
                    print(f"    • {subcat['name']} (ID: {subcat['id']})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 3: Obtener la categoría Mascotas con sus subcategorías
    print("\n3. GET /api/categories/16 (Mascotas con subcategorías)")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/categories/16?include_subcategories=true")
        if response.status_code == 200:
            category = response.json()
            print(f"✓ Categoría: {category['name']} (ID: {category['id']})")
            subcats = category.get('subcategories', [])
            print(f"  Subcategorías: {len(subcats)}")
            for subcat in subcats:
                print(f"    • {subcat['name']} (ID: {subcat['id']})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 4: Obtener subcategorías de Mascotas
    print("\n4. GET /api/categories/16/subcategories")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/categories/16/subcategories")
        if response.status_code == 200:
            subcategories = response.json()
            print(f"✓ Total de subcategorías: {len(subcategories)}")
            for subcat in subcategories:
                print(f"  - {subcat['name']} (ID: {subcat['id']})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    # Test 5: Obtener productos de una subcategoría (Complementos)
    print("\n5. GET /api/products?category_id=27 (Complementos)")
    print("-" * 70)
    try:
        response = requests.get(f"{BASE_URL}/products?category_id=27")
        if response.status_code == 200:
            products = response.json()
            print(f"✓ Total de productos: {len(products)}")
            for prod in products:
                print(f"  - {prod['name']} - ${prod['price']} (Stock: {prod['stock']})")
        else:
            print(f"✗ Error: {response.status_code}")
    except Exception as e:
        print(f"✗ Error: {e}")
    
    print("\n" + "=" * 70)
    print("PRUEBAS COMPLETADAS")
    print("=" * 70)

if __name__ == "__main__":
    print("\nAsegúrate de que el backend esté ejecutándose en http://localhost:5000\n")
    input("Presiona Enter para continuar...")
    test_endpoints()
