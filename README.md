OmegaUp CLI - [![py_version](https://img.shields.io/badge/Python-%E2%89%A5%203.7-blue.svg?style=flat-square&logo=python&logoColor=ffffff)](https://www.python.org/downloads/) ![visitors](https://visitor-badge.glitch.me/badge?page_id=OmegaUp-CLI)
=============


<img align="right" src="https://user-images.githubusercontent.com/40130428/112218277-276c9380-8be9-11eb-8d63-1bbf6d9edfa3.png">

<p align="left">
  <img src="https://img.shields.io/badge/Envios-En%20curso-yellow.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Problemas-En%20curso-yellow.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Cursos-Pendiente-red.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Concursos-Pendiente-red.svg?style=flat-square">
</p>

<p align="justify">
OmegaUp CLI es una interfaz que te permite utilizar OmegaUp desde la linea de comandos. Administra concursos, realiza envios y mucho mas sin tener que abandonar el terminal! El comando <code>ucl</code> permite llamar a la OmegaUp CLI desde cualquier parte en tu terminal. Ejecutar la CLI sin parametros mostrara el menu de ayuda.
</p>

<p align="justify">
  <b>Nuevo:</b> Crea entornos de trabajo, prueba tus codigos con los casos de prueba que provee un problema y mas! Para realizar estas acciones, utiliza el nuevo comando <code>ucl entorno</code>. Si deseas mas información consulta el GIF de demostración. (Menu de ayuda en proceso)
</p>

# Instalación [![release](https://img.shields.io/github/v/release/Apocryphon-X/omegaup-cli?include_prereleases&label=Release&logo=github&style=flat-square)](https://github.com/Apocryphon-X/omegaup-cli/releases)


<p align="justify">
El proyecto se encuentra en fase Alpha, por lo que el codigo actual esta <b>INCOMPLETO</b>. Para descargar la versión en desarrollo, se recomienda instalar la CLI desde el repositorio en lugar de las GH Releases.
</p>

```bash
git clone https://github.com/Apocryphon-X/omegaup-cli    # Clona el repositorio.
cd omegaup-cli                                           # Accede al directorio.
chmod +x install.sh                                      # Otorga permisos de ejecución.
./install.sh                                             # Ejecuta el script de instalación.
```

# Comandos actuales

Para ver una demostración de la CLI en acción, da click [aquí.](https://user-images.githubusercontent.com/40130428/112234477-3a3f9200-8c02-11eb-9086-fb65345f11f6.gif)

|       Comando       |                Descripción             |
|:--------------------|:---------------------------------------|
|        `ucl`        |           Ayuda en general             |
|   `ucl envio`       |       Menu de ayuda para envios        |
|  `ucl envio subir`  |        Realizar un nuevo envio         |
|    `ucl entorno`    |     Ayuda para entornos de trabajo     |
| `ucl entorno crear` |    Crea un nuevo entorno de trabajo    |
| `ucl entorno probar`|   Prueba tu codigo antes de subirlo    |


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
[6]: https://user-images.githubusercontent.com/40130428/112232970-26def780-8bff-11eb-9fd8-579dea4c26c8.gif


<!-- Unused
![Commits per month](https://img.shields.io/github/commit-activity/y/Apocryphon-X/omegaup-cli?label=Commit%20Activity&logo=GitHub&style=flat-square)
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
<p align="justify">
  <img src="https://user-images.githubusercontent.com/40130428/112088737-f7c07b80-8b55-11eb-95a4-bafd26d21771.png">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-%E2%89%A5%203.7-blue.svg?style=flat-square&logo=python&logoColor=ffffff">
  </a>
</p>
<table align="center">
  <tr>
    <th><b>:zap: Demostración (Ubuntu 20.04 - WSL 1)</b></th>
  </td>
  <tr>
    <td><img src="https://user-images.githubusercontent.com/40130428/112093910-db294100-8b5f-11eb-9643-7a51b0846964.gif"></th>
  </tr>
</table>
<p align="justify">
Actualmente la CLI solo a sido probada en Ubuntu 20.04 - WSL 1.
</p>
<img align="left" src="https://user-images.githubusercontent.com/40130428/112227576-80dabf80-8bf5-11eb-824a-744cf3910853.gif">
<table align="right">
  <tr>
    <th><b>:zap: Demostración (Ubuntu 20.04 - WSL 1)</b></th>
  </tr>
  <tr>
    <td><img align="center" src="https://user-images.githubusercontent.com/40130428/112232970-26def780-8bff-11eb-9fd8-579dea4c26c8.gif"></td>
  </tr>
</table>
-->
