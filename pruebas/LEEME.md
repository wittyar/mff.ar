# Pruebas de MFF.ar

Scripts de Playwright contra la app servida por `desktop/lanzador.py`: cada `verif_*.py` levanta la app con una carpeta
de datos nueva (`harness.py`), la maneja como un usuario y compara lo que ve contra modelos escritos aparte de `app.js`.
Imprimen `OK`/`FALLA` por chequeo y terminan con `FALLAS: ninguna` o la lista.

## Requisitos

- Python 3 con `playwright` (y su Chromium) y `Pillow`; `node` (harness lee data.js con node).
- `images/` en la raíz del repo (no se versiona): `python3 pruebas/bajar_imagenes.py` las baja de lo que publica
  datos.json, o sirve un enlace a una carpeta con ellas.
- `work/` (lo que baja `scripts/fetch_all.py --no-portraits`): lo necesitan verif_guia_ficha, verif_marcadores,
  verif_opciones y armar los datos de prueba con el build.

## Rutas y datos

`rutas.py` da `RAIZ` (el repo), `PRUEBAS` (esta carpeta) y `SALIDA` (`pruebas/salida/`, donde van las capturas de
pantalla y las mediciones; git no la sigue). Los datos salen del repo, salvo que `MFF_DATOS` apunte a otra carpeta con
`data.js`, `datos.json`, `docs/` e `images/`: hace falta cuando el código pide un formato de datos que el repo todavía
no publica (antes de que `scripts/actualizar_datos.py` publique los de ese formato). Se arma copiando el repo con `work/` a otra carpeta y
corriendo ahí `python3 scripts/build.py`.

## Correr

```
./pruebas/correr.sh                          # todas, en pruebas/salida/reg
./pruebas/correr.sh reg2 verif_que_hace verif_cmp_efecto
MFF_DATOS=/ruta/datos python3 pruebas/verif_que_hace.py
```

## Las que no corren solas

- Necesitan `dist/` (el instalador y el parche armados: `python3 desktop/construir.py release vX.Y.Z`): verif_programa
  y verif_wine, que además pide la app instalada en el prefijo de Wine `/tmp/wine64pfx` (el de `construir.py`):
  `xvfb-run -a /usr/lib/wine/wine64 dist/TA-GUIANAEL-MFF-X.Y.Z.exe /VERYSILENT /SUPPRESSMSGBOXES /NORESTART`, sin
  `TMPDIR` (Wine 9.0 se cae con ella). verif_actualizacion_real y verif_parche_1xx son de versiones viejas (la 1.0.0 a
  la 1.0.1, la 1.0.18 a la 1.0.19…: verifican la versión de `version.json` o piden archivos que ya no están) y no
  corren con la de hoy; algunas piden argumentos.
- Comparan contra versiones viejas del repo (worktrees que ya no están): verif_filas, verif_export_viejo.
- Necesitan `work/`: verif_guia_ficha, verif_marcadores, verif_opciones; y verif_imagenes, las imágenes reales.
- `liderazgos_api/prueba.py` usa datos de formato 7 de una sesión vieja (`ORIGEN`): hay que pasarle una carpeta.

- verif_formato, verif_lanzador, verif_paginador y verif_servidor_caido usan los datos del repo para sembrar la app: van
  sin `MFF_DATOS` (con datos de otra carpeta del mismo formato, verif_formato falla porque la app no vuelve a bajarlos).

El 9 de octubre de 2026 pasaron las 54 que corren solas: 50 con `MFF_DATOS` (datos de formato 14 con lo de #10) y esas
cuatro con los del repo.
