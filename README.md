# OmegaUp CLI - [![py_version](https://img.shields.io/badge/Python-%E2%89%A5%203.7-blue.svg?style=flat-square&logo=python&logoColor=ffffff)](https://www.python.org/downloads/) 

<!-- ![Commits per month](https://img.shields.io/github/commit-activity/y/Apocryphon-X/omegaup-cli?label=Commit%20Activity&logo=GitHub&style=flat-square)
-->

![Estado](https://img.shields.io/badge/Envios-en%20proceso-yellow.svg?style=flat-square)
![Estado](https://img.shields.io/badge/Perfil-pendiente-red.svg?style=flat-square)
![Estado](https://img.shields.io/badge/Cursos-pendiente-red.svg?style=flat-square)
![Estado](https://img.shields.io/badge/Concursos-pendiente-red.svg?style=flat-square)
![Estado](https://img.shields.io/badge/Problemas-pendiente-red.svg?style=flat-square)

Interfaz para utilizar OmegaUp desde la linea de comandos. Administra concursos, realiza envios y mucho mas sin tener que abandonar el terminal! Ocupa el comando `ucl` para llamar a la CLI de OmegaUp desde cualquier parte. Ejecutar la CLI sin parametros, llamara al menu de ayuda e información.

<p align="center"> 
  <img src="https://user-images.githubusercontent.com/40130428/111728441-8077a880-8832-11eb-9b19-1870bf705d60.gif">
</p>

<p align="center"> <b> Probado en:</b> Ubuntu 20.04 - WSL 1 </p>

# Instalación [![release](https://img.shields.io/github/v/release/Apocryphon-X/omegaup-cli?include_prereleases&label=Release&logo=github&style=flat-square)](https://github.com/Apocryphon-X/omegaup-cli/releases)

Omegaup CLI esta en fase Alpha, por lo que el codigo actual esta **INCOMPLETO.**
```bash
git clone https://github.com/Apocryphon-X/omegaup-cli    # Clona el repositorio.
cd omegaup-cli                                           # Accede al directorio.
chmod +x install.sh                                      # Otorga permisos de ejecución.
./install.sh                                             # Ejecuta el script de instalación.
```

# Características

Listado de cracterísticas **principales** por desarrollar en la OmegaUp CLI. 

- [ ] Administrar concursos y obtener scoreboards.
- [x] Realizar envios a OmegaUp.¹
- [ ] Envio y listado de clarificaciones en problemarios.
- [x] Mostrar veredicto de envios.²
- [ ] Organizar cursos y gestionar usuarios.
- [ ] Administrar, crear o modificar problemas.

---

- ¹ : De momento solo se pueden hacer envios en C++11 (gcc), a problemas por separado.
- ² : Actualmente la CLI solo muestra el veredicto del envio recien subido, sin mostrar datos adicionales.

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
