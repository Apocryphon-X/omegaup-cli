<p align="justify">
  <img src="https://user-images.githubusercontent.com/40130428/112088737-f7c07b80-8b55-11eb-95a4-bafd26d21771.png">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-%E2%89%A5%203.7-blue.svg?style=flat-square&logo=python&logoColor=ffffff">
  </a>
</p>
<p align="justify">
  <img src="https://img.shields.io/badge/Envios-En%20proceso-yellow.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Perfil-Pendiente-red.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Cursos-Pendiente-red.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Concursos-Pendiente-red.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Problemas-Pendiente-red.svg?style=flat-square">
</p>

<!-- ![Commits per month](https://img.shields.io/github/commit-activity/y/Apocryphon-X/omegaup-cli?label=Commit%20Activity&logo=GitHub&style=flat-square)
# OmegaUp CLI - [![py_version]()](https://www.python.org/downloads/) 
<h1 align="center">OmegaUp CLI - <img src="https://img.shields.io/badge/Python-%E2%89%A5%203.7-blue.svg?style=flat-square&logo=python&logoColor=ffffff"></h1>
<table align="right">
  <tr>
    <th><b>:zap: Demostración (Ubuntu 20.04 - WSL 1)</b></th>
  </td>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/40130428/112084456-70233e80-8b4e-11eb-8ebb-04cc088f998d.gif"></th>
  </tr>
</table>
<img align="right" src="https://user-images.githubusercontent.com/40130428/112084456-70233e80-8b4e-11eb-8ebb-04cc088f998d.gif">
-->

<p align="justify">
OmegaUp CLI es una interfaz que te permite utilizar OmegaUp desde la linea de comandos. Administra concursos, realiza envios y mucho mas sin tener que abandonar el terminal! El comando <code>ucl</code> permite llamar a la OmegaUp CLI desde cualquier parte en tu terminal. Ejecutar la CLI sin parametros mostrara el menu de ayuda.
</p>


<table align="center">
  <tr>
    <th><b>:zap: Demostración (Ubuntu 20.04 - WSL 1)</b></th>
  </td>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/40130428/112093420-f8a9db00-8b5e-11eb-8f34-29c85f00eabf.gif"></th>
  </tr>
</table>

<p align="justify">
Ahora la OmegaUp CLI posee la habilidad de crear entornos de trabajo! Obten los datos de un problema mediante su alias e interactua con sus casos de prueba sin dejar la linea de comandos. Para crear un nuevo entorno utiliza el comando <code>ucl entorno crear</code> e ingresa el alias del problema una vez que la CLI te pida el dato. Si deseas probar tu codigo con los casos de prueba, utiliza el comando <code>ucl entorno probar</code> y obtendras los resultados.
</p>

# Instalación [![release](https://img.shields.io/github/v/release/Apocryphon-X/omegaup-cli?include_prereleases&label=Release&logo=github&style=flat-square)](https://github.com/Apocryphon-X/omegaup-cli/releases)

Omegaup CLI esta en fase Alpha, por lo que el codigo actual esta **INCOMPLETO.**
```bash
git clone https://github.com/Apocryphon-X/omegaup-cli    # Clona el repositorio.
cd omegaup-cli                                           # Accede al directorio.
chmod +x install.sh                                      # Otorga permisos de ejecución.
./install.sh                                             # Ejecuta el script de instalación.
```

# Características

Características **principales** que implementa la OmegaUp CLI:

- [ ] Administrar concursos y obtener scoreboards.
- [x] Realizar envios a cursos, problemas y problemarios.¹
- [ ] Uso y recopilación de Clarificaciones.
- [x] Mostrar veredicto de envios recien subidos por el usuario.²
- [ ] Organizar cursos y gestionar participantes.
- [ ] Administrar, crear o modificar problemas.
- [x] Crear "entornos de trabajo" de forma local.

---

1: Actualmente solo se soportan envios en C++11 (gcc), a problemas por separado. <br>
2: Temporalmente, la CLI solo muestra el veredicto del envio recien subido sin mostrar datos adicionales.


# Inspiraciones

- [OmegaUp API¹][1] - *"OmegaUp: Open source platform to learn and improve Computer Science skills."*
- [Codeforces CLI¹][2] - *"A simple command line tool for Codeforces coders."*
- [ProtonVPN Linux CLI¹][3] - *"Linux command-line client for ProtonVPN. Written in Python."*
- [Github CLI¹][4] - *"GitHub’s official command line tool."*
- [CF-Tool¹][5] - *"Codeforces Tool is a command-line interface tool for Codeforces."*

¹ : "OmegaUp CLI" is **not** officially affiliated with this organization or project.

[1]: https://github.com/omegaup/omegaup/blob/master/frontend/server/src/Controllers/README.md
[2]: https://github.com/ahmed-dinar/codeforces-cli
[3]: https://github.com/ProtonVPN/linux-cli
[4]: https://github.com/cli/cli
[5]: https://github.com/xalanq/cf-tool
