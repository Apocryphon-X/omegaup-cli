OmegaUp CLI [![py_version][7]][8]
<img align="right" src="https://user-images.githubusercontent.com/40130428/112218277-276c9380-8be9-11eb-8d63-1bbf6d9edfa3.png">
=============



<p align="left">
  <img src="https://img.shields.io/badge/Envios-En%20curso-yellow.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Problemas-En%20curso-yellow.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Cursos-Pendiente-red.svg?style=flat-square">
  <img src="https://img.shields.io/badge/Concursos-En%20curso-yellow.svg?style=flat-square">
</p>

<p align="justify">
OmegaUp CLI es una interfaz que te permite interactuar con OmegaUp desde la linea de comandos. Actualmente el proyecto se encuentra en fase Alpha por lo que hace falta implementar soporte para muchas secciones de la API. Todo issue y pull request es bienvenido. 
</p>

# Cambios

<p align="justify">
  <ul>
    <li> El parsing de argumentos ahora es gestionado mediante el modulo <a href="https://github.com/pallets/click/"><code>Click</code></a>. </li>
    <li> Las interacciones con la API se realizan por medio de APITokens. </li>
    <li> Se removio <b>temporalmente</b> la función de "entornos". </li>
    <li> Se migro parte de el codigo a <a href="https://github.com/omegaup/libomegaup"><code>libomegaup</code></a>. </li>
  </ul>
</p>

# Instalación [![release][9]][10]


<p align="justify">
  El proyecto se encuentra en fase <it>Alpha</it>, por lo que el codigo actual esta <b>INCOMPLETO</b>. Para descargar la versión en desarrollo, se recomienda instalar la CLI desde el repositorio en GitHub o desde <code>pipx</code> en lugar de las GH Releases.
</p>

### Instalación desde [`pipx`][11]

```bash
pipx install omegaup-cli                                 # Instalación global y segura.
```

### Instalación desde la fuente
```bash
git clone https://github.com/Apocryphon-X/omegaup-cli    # Clona el repositorio.
cd omegaup-cli                                           # Accede al directorio.
./linux-install.sh                                       # Ejecuta el script de instalación.
```

# Grupos de comandos actuales

|       Grupo         |                Descripción             |
|:--------------------|:---------------------------------------|
|        `ucl`        |      Muestra los grupos de comandos    |
|      `ucl run`      |       Menu de ayuda para envios        |
|    `ucl contest`    |        Menu de ayuda para econcursos   |
|    `ucl problem`    |      Menu de ayuda para problemas      |

# Inspiraciones

- [OmegaUp API¹][1]: *"OmegaUp: Open source platform to learn and improve Computer Science skills"*.
- [ProtonVPN Linux CLI¹][3]: *"Linux command-line client for ProtonVPN. Written in Python"*.
- [CF-Tool¹][5]: *"Codeforces Tool is a command-line interface tool for Codeforces"*.
- [Codeforces CLI¹][2]: *"A simple command line tool for Codeforces coders"*.
- [Github CLI¹][4]: *"GitHub’s official command line tool"*.

`¹` : `omegaup-cli` is **not** formally affiliated with this organization or project.



# License

<img align="right" src="https://user-images.githubusercontent.com/40130428/112392193-a253ae00-8cbe-11eb-8a27-729c23729923.png">

<p align="justify">
  <a href="https://github.com/Apocryphon-X/omegaup-cli">Apocryphon-X/omegaup-cli</a> is licensed under the MIT License. A short and simple permissive license with conditions only requiring preservation of copyright and license notices. Licensed works, modifications, and larger works may be distributed under different terms and without source code.
More details can be found in the <a href="https://github.com/Apocryphon-X/omegaup-cli/blob/main/LICENSE.md"><code>LICENSE.md</code></a> file.
</p>

[1]: https://github.com/omegaup/omegaup/blob/master/frontend/server/src/Controllers/README.md
[2]: https://github.com/ahmed-dinar/codeforces-cli
[3]: https://github.com/ProtonVPN/linux-cli
[4]: https://github.com/cli/cli
[5]: https://github.com/xalanq/cf-tool
[6]: https://user-images.githubusercontent.com/40130428/112232970-26def780-8bff-11eb-9fd8-579dea4c26c8.gif
[7]: https://img.shields.io/badge/Python-%E2%89%A5%203.8-blue.svg?style=flat-square&logo=python&logoColor=ffffff
[8]: https://www.python.org/downloads/
[9]: https://img.shields.io/github/v/release/Apocryphon-X/omegaup-cli?include_prereleases&label=Release&logo=github&style=flat-square
[10]: https://github.com/Apocryphon-X/omegaup-cli/releases
[11]: https://pypa.github.io/pipx/

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
