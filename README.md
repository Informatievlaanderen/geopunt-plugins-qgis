Geopunt4QGis
============

![Geopunt for QGIS](images/logogeopunt4Q.png "Geopunt for QGIS")

## Functions

* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/zoek-een-adres-in-qgis"><img src="images/geopuntAddressSmall.png" /> Search an address</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/prik-een-adres-op-kaart-in-qgis"><img src="images/geopuntReverseSmall.png" /> Click an address on the map</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/csv-bestanden-geocoderen-in-qgis"><img src="images/geopuntBatchgeocodeSmall.png" /> Geocode CSV files</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/zoek-een-interessante-plaats-in-qgis"><img src="images/geopuntPoiSmall.png" /> Find a point of interest</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/hoogteprofiel-in-qgis"><img src="images/geopuntElevationSmall.png" /> Elevation profile</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/zoek-een-perceel-in-qgis"><img src="images/geopuntParcelSmall.png" /> Find a parcel</a>  
* <a href="https://www.vlaanderen.be/geopunt/plug-ins/qgis-plug-in/geopunt-catalogus-in-qgis"><img src="images/geopuntDataCatalogusSmall.png" /> Geopunt catalog</a>  


## System Requirements

- QGIS 3.x or higher (compatible with QGIS 4.x from release 2.7 onward)
- Python 3 (bundled with QGIS)
- Any OS capable of running QGIS with Python plugins: Windows, macOS, or Linux
- Python modules `matplotlib` and `numpy`  
  - Included with Windows and Linux QGIS installations  
  - May need manual installation on macOS
- Active internet connection (restricted firewalls may block access to services)

---

## Goals

**Geopunt4QGis – "Geopunt for QGIS"** is a plugin for the [QGIS](https://qgis.org/) open‑source desktop GIS.

The Flemish government geoportal **Geopunt** offers a wide range of web services that can be used freely by third parties, including governments, organisations, and citizens.

Standard map services are based on OGC standards such as **WMS** and **WMTS**, and can easily be added to QGIS. These services are discoverable via the metadata catalogue:

👉 https://metadata.vlaanderen.be/srv/dut/catalog.search  

However, some services are **not standardized** and are only available through REST APIs. While these APIs are convenient for developers, they are not directly usable in desktop GIS software like QGIS.

This plugin bridges that gap by integrating these services into QGIS.

### Included services

- **Geocoding**  
  Based on the Flemish address register:  
  <https://www.vlaanderen.be/digitaal-vlaanderen/onze-diensten-en-platformen/gebouwen-en-adressenregister>  

- **Location search (POI)**  
  ased on datasets linked to the address register (e.g. schools, public services)

- **Traffic obstruction information (GIPOD)**  
  <https://gipod.vlaanderen.be>  

- **Elevation profile**  
  Uses the Digital Elevation Model (DHM Vlaanderen):  
  <https://overheid.vlaanderen.be/informatie-vlaanderen/producten-diensten/digitaal-hoogtemodel>  

- **Parcel search (KADMAP / GRB-based services)**  

- **Metadata catalogue**  
  <https://metadata.vlaanderen.be/srv/dut/catalog.search>

The goal is to make these services accessible for:

- map creation
- spatial analysis
- research workflows
- integration into GIS projects

---

## What is Geopunt?

[Geopunt](https://www.geopunt.be/) is the central gateway to geographic information of the Flemish government.

It provides:

- datasets  
- web services  
- applications  
- metadata catalogues  

for a broad audience, including citizens, GIS professionals, engineers, and policy makers.

All components (metadata, downloads, services, and applications) are integrated into one platform. Geopunt is also the Flemish node of the European Spatial Data Infrastructure and complies with the **INSPIRE Directive**:

👉 https://inspire-geoportal.ec.europa.eu/  

Geopunt is managed within **GDI Flanders** (Geographic Data Infrastructure).  
The operational management is handled by:

👉 https://www.vlaanderen.be/digitaal-vlaanderen  

---

## About the Author

My name is **Kay Warrie**. I am a geospatial data analyst and developer based in Belgium.

I work in the research department of the City of Antwerp. My work includes:

- web mapping (ArcGIS Server, Mapbox)
- desktop GIS (QGIS, ArcGIS)
- INSPIRE-compliant metadata management (GDI Flanders)
- spatial analysis on urban data  

Typical analyses include:

- geocoding and address matching  
- proximity and routing analyses  
- environmental impact studies  
- zoning and permit support  

📧 [Contact me](mailto:kaywarrie@gmail.com)  
🌐 [More about me](http://kgis.be)  

---

## Sources

- <https://www.geopunt.be>  
- <https://www.vlaanderen.be/geopunt>  
- <https://metadata.geopunt.be>  
- <https://www.vlaanderen.be/digitaal-vlaanderen>