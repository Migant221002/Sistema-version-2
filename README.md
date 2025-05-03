√∫# Sistema de Gestión de Café

Este es un sistema de gestión para el control de empleados, fincas y pagos en la recolección de café.

## Características

- Autenticación de usuarios (registro e inicio de sesión)
- Gestión de empleados
- Gestión de fincas
- Asignación de empleados a fincas
- Registro de pagos con generación de recibos imprimibles

## Requisitos Previos

- Node.js (v14 o superior)
- MySQL
- Python 3.x (para el backend)

## Instalación

1. Clonar el repositorio:
```bash
git clone <url-del-repositorio>
cd crudSencilloReact
```

2. Instalar dependencias del frontend:
```bash
npm install
```

3. Instalar dependencias del backend:
```bash
pip install flask flask-cors mysql-connector-python PyJWT werkzeug
```

4. Configurar la base de datos:
- Crear una base de datos MySQL
- Ejecutar el archivo `schema.sql` para crear las tablas necesarias

5. Configurar las variables de entorno:
- Crear un archivo `.env` en la raíz del proyecto con las credenciales de la base de datos

## Ejecución

1. Iniciar el servidor backend:
```bash
python API.py
```

2. Iniciar el frontend:
```bash
npm start
```

3. Acceder a la aplicación en `http://localhost:3000`

## Estructura del Proyecto

```
crudSencilloReact/
├── src/
│   ├── components/
│   │   ├── Auth/
│   │   ├── Empleados/
│   │   ├── Fincas/
│   │   ├── Asignaciones/
│   │   ├── Pagos/
│   │   └── Layout/
│   ├── App.js
│   └── index.js
├── API.py
├── schema.sql
└── package.json
```

## Uso

1. Registrarse como nuevo usuario
2. Iniciar sesión
3. Navegar por los diferentes módulos:
   - Empleados: Registrar y gestionar empleados
   - Fincas: Registrar y gestionar fincas
   - Asignaciones: Asignar empleados a fincas
   - Pagos: Registrar pagos y generar recibos

## Tecnologías Utilizadas

- Frontend:
  - React
  - Material-UI
  - React Router
  - Axios
  - React-to-print

- Backend:
  - Python
  - Flask
  - MySQL
  - JWT para autenticación

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.<br />
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.<br />
You will also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.<br />
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.<br />
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.<br />
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

### Code Splitting

This section has moved here: https://facebook.github.io/create-react-app/docs/code-splitting

### Analyzing the Bundle Size

This section has moved here: https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size

### Making a Progressive Web App

This section has moved here: https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app

### Advanced Configuration

This section has moved here: https://facebook.github.io/create-react-app/docs/advanced-configuration

### Deployment

This section has moved here: https://facebook.github.io/create-react-app/docs/deployment

### `npm run build` fails to minify

This section has moved here: https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify

Prueba_Miguel 2