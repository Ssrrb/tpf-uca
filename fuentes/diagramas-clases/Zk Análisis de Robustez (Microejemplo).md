---
Title: Zk Análisis de Robustez (Microejemplo)
TipoNota: permanente
Área:
  - definir
SubÁrea:
  - definir
tags:
  - definir
dg-publish: true
publish: true
aliases:
  - Microejemplo de Análisis de Robustez
---

## Microejemplo de Análisis de Robustez

### Caso de Uso de Ejemplo

Nombre: Iniciar sesión  
Actor principal: Usuario registrado  
Objetivo: Permitir que el usuario acceda al sistema ingresando credenciales válidas.  

**Flujo principal (simplificado):**  
1. El usuario solicita la página de inicio de sesión.  
2. El sistema muestra el formulario de inicio de sesión.  
3. El usuario ingresa nombre de usuario y contraseña.  
4. El usuario solicita iniciar sesión.  
5. El sistema valida las credenciales.  
6. El sistema concede el acceso y muestra la página principal del usuario.  

### Identificación de Objetos

- Actor:  
  - Usuario  

- Objetos de frontera (límite / interfaz):  
  - PantallaInicioSesion  
  - PantallaPrincipalUsuario  

- Objetos de entidad (modelo / datos):  
  - UsuarioSistema  
  - CredencialAcceso  

- Objetos de control (lógica de caso de uso):  
  - ControlIniciarSesion  

### **Borrador de colaboraciones**  

- Usuario → PantallaInicioSesion: solicitarPantalla()  
- PantallaInicioSesion → Usuario: mostrarFormulario()  
- Usuario → PantallaInicioSesion: enviarCredenciales(usuario, contraseña)  
- PantallaInicioSesion → ControlIniciarSesion: solicitarAutenticacion(usuario, contraseña)  
- ControlIniciarSesion → UsuarioSistema: buscarPorNombreUsuario(usuario)  
- ControlIniciarSesion → CredencialAcceso: validar(contraseña)  
- ControlIniciarSesion → PantallaPrincipalUsuario: prepararVista(usuarioAutenticado)  
- PantallaPrincipalUsuario → Usuario: mostrarPantallaPrincipal()  

### Explicación
Este microejemplo ilustra cómo el análisis de robustez ([[Zk Ref larmanUMLPatronesIntroduccion2010|Larman, 2010]]): 

- obliga a identificar explícitamente la frontera (pantallas), el control (ControlIniciarSesion) y las entidades (UsuarioSistema, CredencialAcceso);  
   
- facilita la transición directa desde el texto del caso de uso hacia un [[Zk Modelo Conceptual del UML (Diagrama de Secuencia)|diagrama de secuencia]] que respeta la separación [[Zk Modelo (MVC)|Modelo–Vista–Controlador]].

### Enlaces Sugeridos

- [[Zk Análisis de Robustez en el Proceso de Análisis y Diseño Orientado a Objetos|Análisis de Robustez en el Proceso de Análisis y Diseño Orientado a Objetos]]
