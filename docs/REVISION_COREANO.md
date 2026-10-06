# Revisión de las notas de actualización: inglés contra coreano (#3)

Revisión a mano del 6 de octubre de 2026 sobre `docs/NOTAS_COREANO.md` (lo genera `scripts/cotejo_ko.py`). El coreano
es el original. De 191 notas en inglés, 177 tienen par en el café coreano (`fuentes/cafe/`: 176 notas, una acompaña a
dos en inglés); se comparan 175 pares (el de la 1.3.1 no: el foro en inglés no deja leerla) y 28 tienen algún porcentaje
o algún segundo distinto. Abajo, cada uno leído en los dos idiomas y clasificado. La comparación automática
solo mira números: una diferencia de palabras sin números (un nombre, un efecto) no aparece. Y cuando las dos notas tienen
la misma cantidad de secciones las compara en orden, aunque una sección no sea la misma (2016-12-06).

## El inglés traduce mal o deja afuera algo del coreano

| Fecha | Nota | Coreano (original) | Inglés |
|---|---|---|---|
| 2015-12-14 | [1.8.0](https://forum.netmarble.com/futurefight_en/view/2196/173001) · [café](https://cafe.naver.com/futurefight/328127) | Red Skull «내성 증가» (Military Resistance): se activa con HP 40% o menos (antes 30%). Red Hulk «방사선 흡수» (Absorb Radiation): con HP 50% (antes 30%). | «Activates faster», sin los valores. |
| 2016-03-15 | [2.0.0](https://forum.netmarble.com/futurefight_en/view/2196/319471) · [café](https://cafe.naver.com/futurefight/450400) | Punto 15: se ponen topes a los stats («lo que pasa del tope no cuenta»): resistencias a fuego, frío, electricidad, veneno y mente, de 75% a 200%; tasa de recuperación, de 200% a 250%. | No está. |
| 2016-03-15 | idem | Jefe mundial: al cambiar de héroe (tag) solo se aplica 1 segundo de invencibilidad. | Solo dice que la curación al cambiar no está. |
| 2020-10-27 | [10/27](https://forum.netmarble.com/futurefight_en/view/2196/1654097) · [café](https://cafe.naver.com/futurefight/2610003) | C.T.P. nuevo, efecto «간파»: la barra se carga al recibir golpes y, llena (100%), se activa siempre al recibir un golpe; cancela la skill del primer rival que pegó. | «The gauge charges when attacked», sin el «siempre al 100%» ni el «primer rival». |
| 2021-01-05 | [1/5](https://forum.netmarble.com/futurefight_en/view/2196/1675721) · [café](https://cafe.naver.com/futurefight/2652062) | Agregado del 6 de enero: el uniforme nuevo de Loki suma a la skill activa 5 Parálisis (ignora inmunidad) de 2 s. | No está. |
| 2021-04-20 | [4/20](https://forum.netmarble.com/futurefight_en/view/2196/1700347) · [café](https://cafe.naver.com/futurefight/2698916) | Agregado del 30 de abril: Mister Fantastic <Maker>, skill activa 3: el aturdimiento dura 2 s (estaba escrito 1 s). | No está. |
| 2021-07-13 | [7/14](https://forum.netmarble.com/futurefight_en/view/2196/1719250) · [café](https://cafe.naver.com/futurefight/2748064) | Black Panther <3099>, ultimate de Tier-3: se le saca «prob. de crítico +5%» (entre otros) y, a cambio, aumentan la cantidad de golpes y la **velocidad de ataque**. | «Critical Rate by +%%» (sin el valor) y «the number of hits and the **skill duration**»: la duración no es lo que dice el coreano. |

## El inglés trae algo que el coreano no

Casi siempre correcciones del texto en inglés hechas después (el error era de la traducción) o datos que el coreano
muestra en una imagen.

| Fecha | Nota | Inglés |
|---|---|---|
| 2016-07-13 | [2.3.0](https://forum.netmarble.com/futurefight_en/view/2196/464430) | Captain Marvel y Lash: «+10% por cada 1% de daño acumulado»; el coreano dice «n%», sin el valor. |
| 2016-12-06 | [2.7](https://forum.netmarble.com/futurefight_en/view/2196/620048) | Una sección «Character Balancing» (Captain Marvel: «Binary Explosion» con inmunidad a todo daño 5 s; al terminar «Radiant Form» las recargas ya no se refrescan 1 s; Thor y otros). El texto coreano no la tiene: su sección de ese lugar es «기타 게임 개선사항» (otras mejoras). |
| 2017-08-08 | [3.3](https://forum.netmarble.com/futurefight_en/view/2196/890827) | Spider-Man 2099: 75% transparente e invencible 2 s; Ancient One: transparencia 75% y +10% de evasión. No está en el texto coreano. [Probable] en una imagen. |
| 2017-09-12 | [3.4.0](https://forum.netmarble.com/futurefight_en/view/2196/921508) | Jean Grey, antes y después (+3% y +5%). No está en el texto coreano. [Probable] en una imagen. |
| 2021-08-17 | [8/17](https://forum.netmarble.com/futurefight_en/view/2196/1725398) | Agregado del 12 de noviembre: War Machine <3099>, skill activa 3, «+11%» estaba mal escrito: es +13% por cada 1% de daño acumulado. |
| 2021-09-07 | [9/7](https://forum.netmarble.com/futurefight_en/view/2196/1728043) | Agregado del 15 de noviembre: Shang-Chi <Shang-Chi and the Legend of the Ten Rings>, skill activa 3: recupera 50% de la vida máxima (estaba escrito 60%). |
| 2022-03-16 | [3/16](https://forum.netmarble.com/futurefight_en/view/2196/1749392) | Artefacto: «+0,2% de daño básico por cada 1% de prob. de crítico», antes y después. No está en el texto coreano. |
| 2022-09-06 | [9/6](https://forum.netmarble.com/futurefight_en/view/2196/1768099) | Corrección: un valor del aviso decía 20% y es 65%. |
| 2023-02-14 | [2/14](https://forum.netmarble.com/futurefight_en/view/2196/1783294) | M.O.D.O.K., Tier-3: el daño pasa de energía a mente (180% del ataque de energía). No está en el texto coreano. |
| 2023-07-11 | [7/11](https://forum.netmarble.com/futurefight_en/view/2196/1794321) | Black Widow, Tier-4: el texto de la skill se aclara («el efecto no cambia»). Corrección de la traducción. |
| 2024-10-15 | [10/15](https://forum.netmarble.com/futurefight_en/view/2196/1825274) | Cromo «Marvel Zombies Return (2009) #1»: su opción de vida +20% se acumula con la misma de otros cromos. El coreano dice lo mismo sin el valor. |

## Sin diferencia real

- Descuentos, recompensas, compensaciones y horarios de reinicio (00:00): 2018-05-29, 2018-07-02, 2019-09-09,
  2019-10-22, 2019-12-03 (la compensación del 99% es del servidor global), 2020-04-21, 2021-04-20 (las 10 zonas del
  envío), 2022-07-05, 2024-10-15 (el millaje), 2016-08-16, 2016-12-06 (el modo por puntos del 100%), 2017-08-08 (el
  100% de las recompensas).
- 2020-02-11: los dos dicen 10 s (el coreano lo repite en una aclaración de formato).
- 2025-04-28: «150% de la cantidad» en coreano y «+50%» en inglés dicen lo mismo.

## Pares que no son

- 2015-11-18: la nota «1.7 Patch Notes» en inglés (los cambios de balance) quedó con un parche coreano del día siguiente:
  el detalle coreano de la 1.7 no está en los tableros del café. Las diferencias de ese par no dicen nada.
- 14 notas en inglés no tienen par (la lista, en `docs/NOTAS_COREANO.md`): sus notas coreanas no están en los tableros
  4 y 141 del café, ni en «공지사항» (5).

## Qué se puede hacer con esto

- Los topes de resistencias (200%) y de tasa de recuperación (250%) que usa la app salen de la guía de thanosvibs
  (`scripts/contenido/guia.json`); la nota coreana del 15 de marzo de 2016 los confirma con una fuente oficial.
- Los textos del histórico en la app (`MFF_HISTORICO`) son los de las notas en inglés: en los casos de la primera tabla,
  el coreano dice más. Desde la 1.0.33 (formato 11), esos casos llevan en la app un «≠» junto a la nota con lo que dice el
  coreano (`scripts/contenido/dudas.json`, tipo `nota`). Mostrar el texto coreano entero sigue en #42.
