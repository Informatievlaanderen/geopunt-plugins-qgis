# Geopunt4QGis

## Functies

*  Zoek een adres
*  Prik een adres op de kaart
*  CSV-bestanden geocoderen
*  Zoek een interessante plaats (POI)
*  Hoogteprofiel
*  Zoek een perceel
*  Geopunt catalogus

## Systeemvereisten

* QGIS 3.x of hoger (compatibel met QGIS 4.x vanaf release 2.7)
* Python 3 (gebundeld met QGIS)
* Elk besturingssysteem dat QGIS met Python plug-ins kan draaien: Windows, macOS of Linux
* Python modules `matplotlib` en `numpy`
* Inbegrepen bij Windows en Linux QGIS-installaties
* Vereist mogelijk handmatige installatie op macOS


* Actieve internetverbinding (strikte firewalls kunnen de toegang tot diensten blokkeren)

---

## Doelstellingen

**Geopunt4QGis – "Geopunt voor QGIS"** is een plug-in voor de open-source desktop GIS [QGIS](https://qgis.org/).

Het geoportaal van de Vlaamse overheid **Geopunt** biedt een breed scala aan webservices die vrij kunnen worden gebruikt door derden, inclusief overheden, organisaties en burgers.

Standaard kaartdiensten zijn gebaseerd op OGC-standaarden zoals **WMS** en **WMTS**, en kunnen eenvoudig worden toegevoegd in QGIS. Deze diensten zijn vindbaar via de metadatacatalogus:

👉 https://metadata.vlaanderen.be/srv/dut/catalog.search

Sommige diensten zijn echter **niet gestandaardiseerd** en zijn enkel beschikbaar via REST API's. Hoewel deze API's handig zijn voor ontwikkelaars, zijn ze niet direct bruikbaar in desktop GIS-software zoals QGIS.

Deze plug-in overbrugt die kloof door deze diensten te integreren in QGIS.

### Inbegrepen diensten

* **Geocodering**
Gebaseerd op het Vlaamse gebouwen- en adressenregister:
[https://www.vlaanderen.be/digitaal-vlaanderen/onze-diensten-en-platformen/gebouwen-en-adressenregister](https://www.vlaanderen.be/digitaal-vlaanderen/onze-diensten-en-platformen/gebouwen-en-adressenregister)
* **Locatie zoeken (POI)**
Gebaseerd op datasets gekoppeld aan het adressenregister (bijv. scholen, openbare diensten)
* **Informatie over verkeershinder (GIPOD)**
[https://gipod.vlaanderen.be](https://gipod.vlaanderen.be)
* **Hoogteprofiel**
Gebruikt het Digitaal Hoogtemodel (DHM Vlaanderen):
[https://overheid.vlaanderen.be/informatie-vlaanderen/producten-diensten/digitaal-hoogtemodel](https://overheid.vlaanderen.be/informatie-vlaanderen/producten-diensten/digitaal-hoogtemodel)
* **Perceel zoeken (KADMAP / GRB-gebaseerde diensten)**
* **Metadatacatalogus**
[https://metadata.vlaanderen.be/srv/dut/catalog.search](https://metadata.vlaanderen.be/srv/dut/catalog.search)

Het doel is om deze diensten toegankelijk te maken voor:

* het maken van kaarten
* ruimtelijke analyses
* onderzoeksworkflows
* integratie in GIS-projecten

---

## Wat is Geopunt?

[Geopunt](https://www.geopunt.be/) is de centrale toegangspoort tot geografische informatie van de Vlaamse overheid.

Het biedt:

* datasets
* webservices
* toepassingen
* metadatacatalogi

voor een breed publiek, waaronder burgers, GIS-professionals, ingenieurs en beleidsmakers.

Alle componenten (metadata, downloads, diensten en toepassingen) zijn geïntegreerd in één platform. Geopunt is ook het Vlaamse knooppunt van de Europese Ruimtelijke Data Infrastructuur en voldoet aan de **INSPIRE-richtlijn**:

👉 https://inspire-geoportal.ec.europa.eu/

Geopunt wordt beheerd binnen **GDI-Vlaanderen** (Geografische Data Infrastructuur).

Het operationele beheer wordt uitgevoerd door:

👉 https://www.vlaanderen.be/digitaal-vlaanderen

---

## Over de auteur

Mijn naam is **Kay Warrie**. Ik ben een ruimtelijke data-analist en ontwikkelaar, gevestigd in België.

Ik werk op de onderzoeksafdeling van de stad Antwerpen. Mijn werk omvat:

* web mapping (ArcGIS Server, Mapbox)
* desktop GIS (QGIS, ArcGIS)
* INSPIRE-conforme metadata-beheer (GDI-Vlaanderen)
* ruimtelijke analyse van stedelijke data

Typische analyses omvatten:

* geocodering en adresmatching
* nabijheids- en routeanalyses
* milieueffectstudies
* ondersteuning bij ruimtelijke ordening en vergunningen

📧 [Neem contact op](https://www.google.com/search?q=mailto%3Akaywarrie%40gmail.com)

🌐 [Meer over mij](http://kgis.be)

---

## Bronnen

* [https://www.geopunt.be](https://www.geopunt.be)
* [https://www.vlaanderen.be/geopunt](https://www.vlaanderen.be/geopunt)
* [https://metadata.geopunt.be](https://metadata.geopunt.be)
* [https://www.vlaanderen.be/digitaal-vlaanderen](https://www.vlaanderen.be/digitaal-vlaanderen)