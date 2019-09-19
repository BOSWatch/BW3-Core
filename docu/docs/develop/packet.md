## BOSWatch Packet Format

Ein BOSWatch Datenpaket wird in einem Python Dict abgebildet. In der nachfolgenden Tabelle sind die genutzten Felder abgebildet.

### Allgemeine Informationen

|Feldname|FMS|POCSAG|ZVEI|MSG|Wildcard|Beschreibung|
|--------|:-:|:----:|:--:|:-:|--------|------------|
|serverName|X|X|X|X|`{SNAME}`|Name der BOSWatch Server Instanz|
|serverVersion|X|X|X|X|`{SVERS}`||
|serverBuildDate|X|X|X|X|`{SDATE}`||
|serverBranch|X|X|X|X|`{SBRCH}`||
|clientName|X|X|X|X|`{CNAME}`|Name der BOSWatch Client Instanz|
|clientIP|X|X|X|X|`{CIP}`||
|clientVersion|X|X|X|X|`{CVERS}`||
|clientBuildDate|X|X|X|X|`{CDATE}`||
|clientBranch|X|X|X|X|`{CBRCH}`||
|inputSource|X|X|X|X|`{INSRC}`|(sdr, audio)|
|timestamp|X|X|X|X|`{TIMES}`||
|frequency|X|X|X|X|`{FREQ}`||
|mode|X|X|X|X|`{MODE}`|(fms, pocsag, zvei, msg)|
|descriptionShort|X|X|X||`{DESCS}`|Kann aus optinalem CSV File geladen werden|
|descriptionLong|X|X|X||`{DESCL}`|Kann aus optinalem CSV File geladen werden|

### Speziell für POCSAG

|Feldname|FMS|POCSAG|ZVEI|MSG|Wildcard|Beschreibung|
|--------|:-:|:----:|:--:|:-:|--------|------------|
|bitrate||X|||`{BIT}`||
|ric||X|||`{RIC}`||
|subric||X|||`{SRIC}`|(1, 2, 3, 4)|
|subricText||X|||`{SRICT}`|(a, b, c, d)|
|message||X||X|`{MSG}`|Kann außerdem für ein Message Paket genutzt werden|

### Speziell für ZVEI

|Feldname|FMS|POCSAG|ZVEI|MSG|Wildcard|Beschreibung|
|--------|:-:|:----:|:--:|:-:|--------|------------|
|tone|||X||`{TONE}`|5-Ton Sequenz nach ZVEI|

### Speziell für FMS

|Feldname|FMS|POCSAG|ZVEI|MSG|Wildcard|Beschreibung|
|--------|:-:|:----:|:--:|:-:|--------|------------|
|fms|X||||`{FMS}`||
|service|X||||`{SERV}`||
|country|X||||`{COUNT}`||
|location|X||||`{LOC}`||
|vehicle|X||||`{VEC}`||
|status|X||||`{STAT}`||
|direction|X||||`{DIR}`||
|dirextionText|X||||`{DIRT}`|(Fhz->Lst, Lst->Fhz)|
|vehicle|X||||`{VEC}`||
|vehicle|X||||`{VEC}`||
|tacticalInfo|X||||`{TACI}`|(I, II, III, IV)|

### Weitere Wildcards
- `{BR}` - Zeilenumbruch `\r\n`
- `{LPAR}` - öffnende Klammer `(`
- `{RPAR}` - schließende Klammer `)`
- `{TIME}` - Aktueller zeitstempel
