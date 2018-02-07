# shopping_cart
Es un sencillo carrito de compras, que permite:
- Listar elementos(cursos) del carrito de compras.
- Agregar cursos al carrito de compras.
- Proceder con el carrito de compras.

## Instalación

#### Clonar el proyecto
```bash
https://github.com/nblasco/shopping_cart.git
cd shopping_cart/
```

#### Crear entorno virtual y activarlo
```bash
virtualenv venv --python=python3.5
source venv/bin/activate
```

#### Instalar requerimientos
```bash
pip install -r requirements.txt
```

## Configuración

#### Crear archivo con las variables de entorno
Crear archivo ```.env``` y agregar el siguiente contenido
```
# Configurar modo de depuración
DJANGO_DEBUG=True

# Configurar clave secreta de django
DJANGO_SECRET_KEY='xxxxxxxxxx'
```

#### Migrar la aplicación
```bash
python manage.py migrate
```

#### Datos Iniciales
Cargar datos para crear usuarios y roles
```bash
python manage.py loaddata cart/fixtures/user.json
python manage.py loaddata cart/fixtures/item.json
```

## Despliegue
#### Correr django
```bash
python manage.py runserver
```
## Usuarios de prueba
#### Administrador de django:
	usuario: admin
	clave: shop_1234

#### Usuario:
	usuario: norma
	clave: n_123456





