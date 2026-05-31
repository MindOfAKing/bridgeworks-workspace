# GEO Optimalizációs Ajánlat
## Misi's Gin: Láthatóság a mesterséges intelligencia keresőkben

**Készítette:** BridgeWorks
**Címzett:** Kenyeres Mihály, Misi's Gin (Kenyeres Mihály E.V.)
**Dátum:** 2026.05.31.
**Érvényes:** 2026.06.30-ig
**Hivatkozás:** GEO-PROP-260531-misisgin

---

## Vezetői összefoglaló

A Misi's Gin egy díjnyertes, Budapesten készülő kézműves gin, Kenyeres Mihály alkotása. A márka hitelessége valós: arany érem a World Gin Awardson, Magyarország országos győztes cím, TasteAtlas adatlap, és több mint tíz magyar viszonteladó forgalmazza a terméket.

A 2026.05.31-én készült GEO auditunk a weboldalt **44/100 pontra (Gyenge)** értékeli. A probléma nem a márka. A probléma az, hogy a weboldal szinte semmit nem ad a mesterséges intelligencia (MI) asszisztenseknek, két esetben pedig kifejezetten kizárja őket.

A három legsürgősebb probléma:

1. **A ChatGPT és a Claude le van tiltva a szerveren.** Az oldal hibaüzenetet ad az OpenAI és az Anthropic robotjainak. A két legtöbbet használt MI asszisztens szó szerint nem tudja elolvasni az oldalt, így nem tudja ajánlani a Misi's Gint, amikor valaki magyar kézműves gint keres.
2. **Az oldalon nincs strukturált adat.** Az MI számára nincs gépileg olvasható információ a márkáról, a termékről, a díjakról vagy a készítőről. Amikor egy MI leírja a gint, a viszonteladók oldalairól dolgozik, nem az Önéről.
3. **Nincs korhatár-ellenőrzés, adatvédelmi tájékoztató és impresszum.** Egy hat piacon értékesítő alkoholos oldalnál ez jogi és bizalmi hiányosság, és az MI modellek a hiányzó bizalmi jeleket gyengébb minőségként értelmezik.

Javaslatunk: egy egyszeri **GEO Alapozás**, amely minden kritikus és magas prioritású hibát megold, valamint egy opcionális, könnyű havi csomag a hosszabb távon megtérülő, oldalon kívüli munkához.

---

## Miért fontos ez a Misi's Gin számára

Az emberek egyre gyakrabban tesznek fel a ChatGPT-nek, a Google MI-válaszainak és a Perplexitynek olyan kérdéseket, mint "legjobb magyar kézműves gin", "gin ajándék Budapest", vagy "díjnyertes kis tételű gin". Egy aranyérmes ginnek meg kellene nyernie ezeket a válaszokat. Jelenleg a Misi's szinte láthatatlan bennük, helyette a gint forgalmazó viszonteladók jelennek meg. Ez azt jelenti, hogy a felfedezés, és gyakran a vásárlás is, egy közvetítőn vagy egy versenytárson keresztül történik.

A megoldás nagyrészt technikai és egyszeri. Amint az MI asszisztensek el tudják olvasni az oldalt, és a márka tényei gépileg olvashatóvá válnak, a díjak elkezdenek dolgozni a márkáért az MI válaszokon belül is.

---

## Az audit eredményei

| Kategória | Pontszám | Prioritás |
|---|---|---|
| MI idézhetőség és láthatóság | 38/100 | Magas |
| Márkatekintély jelei | 58/100 | Közepes |
| Tartalom minősége és E-E-A-T | 52/100 | Közepes |
| Technikai alapok | 58/100 | Magas |
| Strukturált adatok | 8/100 | Magas |
| Platform-optimalizáció | 31/100 | Magas |
| **Összesített GEO pontszám** | **44/100** | **Gyenge** |

### Kritikus problémák

**1. A ChatGPT és a Claude robotjai hibaüzenetet kapnak**
Amit találtunk: a GPTBot és a ClaudeBot 404-es hibát kap, miközben a normál látogatók megkapják az oldalt. Egy tűzfal-szabály blokkolja őket.
Üzleti hatás: a két legnagyobb MI asszisztens egyáltalán nem látja és nem idézi az oldalt.
Megoldásunk: mindkét robot engedélyezése és ellenőrzése.

**2. Sehol nincs strukturált adat**
Amit találtunk: nulla üzleti séma. Az MI számára nincs gépileg olvasható azonosító a márkáról, termékről, díjakról vagy készítőről.
Üzleti hatás: az MI harmadik felek oldalairól írja le a gint, nem a márka oldaláról.
Megoldásunk: teljes JSON-LD séma (Lepárló, Termék, Személy, Recept, díjak, közösségi profilok).

**3. Hiányzó jogi és megfelelőségi oldalak**
Amit találtunk: nincs korhatár-ellenőrzés, adatvédelmi tájékoztató és impresszum egy hat piacon működő alkoholos oldalon.
Üzleti hatás: jogi kockázat és bizalmi pontlevonás az MI minőségi jeleiben.
Megoldásunk: korhatár-kapu, adatvédelmi tájékoztató és impresszum hozzáadása, valamint a meglévő cégadatok megfelelő megjelenítése.

### Magas prioritású problémák
- Vékony, csak történet-alapú tartalom, termékadatok nélkül (alkoholfok, botanikumok, kiszerelés, ár) a márka saját oldalain
- Nincs GYIK, amely a vásárlók valós MI-kérdéseire válaszolna
- Hibás oldaltérkép (3 URL, egy 2015-ös dátum, mind a hat nyelvi verzió hiányzik)
- A díjak említve vannak, de nincsenek alátámasztva, és a legerősebb 2022-es díj egyáltalán nincs feltüntetve
- Nincs meta leírás, nincsenek közösségi előnézeti címkék

---

## Megoldásunk

### GEO Alapozás (egyszeri)
**~550 000 HUF (~€1 400) + ÁFA**

Egy meghatározott projekt, körülbelül 4-6 hét, amely minden kritikus és magas prioritású hibát megold:

- A GPTBot és a ClaudeBot feloldása, hozzáférés ellenőrzése minden nagyobb MI robotnak
- Teljes JSON-LD séma: Lepárló/Helyi vállalkozás, Termék, Személy (alapító), Recept a koktélokhoz, díjak és közösségi profilok
- Az EN és HU főoldal újraírása "válasz-először" szerkezetben, világos termékadat-blokkal (alkoholfok, botanikumok, kiszerelés, eredet)
- GYIK szekció a legfontosabb gin-kérdésekkel
- Az oldaltérkép újraépítése mind a hat nyelvvel és helyes dátumokkal, a robots.txt oldaltérkép-sor hozzáadása
- A hiányzó 2022-es díj hozzáadása és a díjak hivatkozása a díjazó szervezetekre
- Korhatár-ellenőrzés, adatvédelmi tájékoztató és impresszum hozzáadása
- Meta leírások és közösségi előnézeti címkék nyelvenként
- llms.txt közzététele

Várható eredmény: a GEO pontszám jelentős javulása, az oldal pedig olvashatóvá és idézhetővé válik minden nagyobb MI asszisztens számára. A munkát és a módszertant vállaljuk, nem egy konkrét pontszámot.

### Láthatósági Gondozás (opcionális havi csomag)
**~135 000 HUF/hó (~€350) + ÁFA, minimum 3 hónap**

A hosszabb távon megtérülő, oldalon kívüli munkához:

- Wikidata adatlap előkészítése és benyújtása a márkához és az alapítóhoz (a közzététel a platform döntésétől függ)
- Google Cégprofil beállítása és optimalizálása (Lepárló, Budapest)
- Havi egy-két tartalom vagy koktélrecept megfelelő sémával
- Hiteles részvétel a releváns Reddit- és magyar szeszközösségekben, az egyes platformok szabályainak megfelelően
- Havi MI-láthatósági ellenőrzés és rövid haladási összefoglaló

---

## Befektetési összefoglaló

| Tétel | HUF | EUR (kb.) |
|---|---|---|
| GEO Alapozás (egyszeri) | 550 000 | €1 400 |
| Láthatósági Gondozás (havonta, opcionális) | 135 000 | €350 |
| Alapozás + 3 hónap Gondozás | 955 000 | €2 450 |

Az árak nem tartalmazzák az ÁFA-t. Számlázás a szamlazz.hu rendszerén keresztül.

*Az EUR értékek tájékoztató jellegűek, kb. 390 HUF/EUR árfolyamon.*

---

## Következő lépések

1. Az eredmények és az ajánlat átnézése
2. Egy rövid hívás, ahol közösen átbeszéljük az auditot
3. A munka terjedelmének és kezdési időpontjának egyeztetése
4. Olvasási hozzáférés a Google Search Console-hoz, ha van (hasznos, de nem kötelező)

Ez az ajánlat 2026.06.30-ig érvényes.

---

*office@bridgeworks.agency · bridgeworks.agency*
