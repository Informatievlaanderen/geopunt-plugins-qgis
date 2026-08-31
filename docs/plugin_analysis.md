# Geopunt4QGIS Plugin — Essential Update Suggestions

## Overview

**geopunt4Qgis v2.7.0.4** is a well-structured QGIS 4.x plugin that bridges Flemish government REST APIs (Digitaal Vlaanderen) into QGIS. The codebase was recently migrated from QGIS 3.x. The following issues and improvements are organized by priority.

---

## 🔴 Critical Bugs

### 1. `fetch_non_blocking` callback condition is inverted
[`tools/web.py` L54–56](file:///v:/project/geopunt-plugins-qgis/tools/web.py#L54-L56)

```diff
- fetcher.finished.connect(
-     lambda: callback(fetcher.contentAsString()) if fetcher.reply().error() !=0
-                                                 else onerror(fetcher.reply().errorString())
- )
+ fetcher.finished.connect(
+     lambda: callback(fetcher.contentAsString()) if fetcher.reply().error() == 0
+                                                 else onerror(fetcher.reply().errorString())
+ )
```
The condition `!= 0` means the success callback fires on **error** and the error handler fires on **success** — a logic inversion.

---

### 2. Settings dialog: `samplesSaveMemory` uses `.value()` instead of `.setValue()`
[`geopunt4QgisSettingsdialog.py` L204](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisSettingsdialog.py#L204)

```diff
- self.s.value("geopunt4qgis/samplesSaveMemory", samplesSaveMemory)
+ self.s.setValue("geopunt4qgis/samplesSaveMemory", samplesSaveMemory)
```
The elevation "save to memory" preference is silently never persisted.

---

### 3. Settings dialog: GIPOD settings copy POI values instead of GIPOD values
[`geopunt4QgisSettingsdialog.py` L96–99](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisSettingsdialog.py#L96-L99)

```diff
  gipodSavetoFile = int( self.s.value("geopunt4qgis/gipodSavetoFile" , 1))
- self.ui.gipodSavetoFileChk.setChecked(poiSavetoFile)   # wrong variable!
+ self.ui.gipodSavetoFileChk.setChecked(gipodSavetoFile)

  gipodSaveMemory = int( self.s.value("geopunt4qgis/gipodSaveMemory" , 0))
- self.ui.gipodSaveMemoryChk.setChecked(poiSaveMemory)   # wrong variable!
+ self.ui.gipodSaveMemoryChk.setChecked(gipodSaveMemory)
```

---

### 4. `reverseAdresCallback` uses deprecated `QgsMessageBar.INFO` / `.WARNING` constants
[`geopunt4qgis.py` L300, L304](file:///v:/project/geopunt-plugins-qgis/geopunt4qgis.py#L297-L307)

```diff
- level=QgsMessageBar.INFO, duration=3)
+ level=Qgis.Info, duration=3)

- adres, level=QgsMessageBar.WARNING)
+ adres, level=Qgis.Warning)
```
`QgsMessageBar.INFO/WARNING` were removed in QGIS 4; `Qgis.Info/Warning` is correct (already used correctly elsewhere in the same file).

---

### 5. `gipod.py` has a duplicate `allManifestations` method that shadows the workassignment version
[`geopunt/gipod.py` L65–73 & L110–119](file:///v:/project/geopunt-plugins-qgis/geopunt/gipod.py#L65-L119)

The first `allManifestations` (for workassignments) is silently overwritten by the second one. The first should be renamed `allWorkassignments`.

---

## 🟠 API / Compatibility Issues

### 6. GIPOD API v1 is deprecated — upgrade to v2
[`geopunt/gipod.py` L6](file:///v:/project/geopunt-plugins-qgis/geopunt/gipod.py#L6)

```diff
- self.baseUri = 'https://api.gipod.vlaanderen.be/ws/v1/'
+ self.baseUri = 'https://api.gipod.vlaanderen.be/ws/v2/'
```
The v1 endpoint is end-of-life. The v2 API uses a different response schema (GeoJSON features vs. bare arrays), so the consumer dialogs need updating too.

---

### 7. `QgsVectorFileWriter.writeAsVectorFormat` is deprecated in QGIS 4
[`tools/geometry.py` L185–195](file:///v:/project/geopunt-plugins-qgis/tools/geometry.py#L185-L195)

Replace with the new `QgsVectorFileWriter.writeAsVectorFormatV3()` / `QgsVectorFileWriter.create()` API or use `QgsVectorFileWriter.writeAsVectorFormatV2`.

---

### 8. `QgsPalLayerSettings.Free` placement enum may have changed
[`tools/geometry.py` L215](file:///v:/project/geopunt-plugins-qgis/tools/geometry.py#L215)

In QGIS 4 the placement enum was reorganised under `Qgis.LabelPlacement`. Verify and update if needed.

---

## 🟡 Architecture & Code Quality

### 9. Blocking network calls freeze the QGIS UI
All API calls go through [`tools/web.py::getUrlData`](file:///v:/project/geopunt-plugins-qgis/tools/web.py#L8) which uses `QgsBlockingNetworkRequest`. This blocks the UI thread during every geocode/parcel/elevation query. For batch operations (`geopunt4QgisBatchGeoCode.py`) this is especially bad. 

**Recommendation:** Move batch and catalog operations to `QgsTask` + `QgsTaskManager` with a progress bar, keeping the non-blocking `fetch_non_blocking` helper for interactive searches once its bug (item 1) is fixed.

---

### 10. `layernameValid()` is copy-pasted across 3 dialogs
The same `layernameValid()` method appears verbatim in:
- [`geopunt4QgisAdresdialog.py` L193](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisAdresdialog.py#L193)
- [`geopunt4QgisBatchGeoCode.py` L146](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisBatchGeoCode.py#L146)
- [`geopunt4QgisElevation.py` L222](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisElevation.py#L222)

Extract to a shared utility function in `tools/`.

---

### 11. Dialogs are instantiated at plugin startup (not lazily)
[`geopunt4qgis.py` L37–45](file:///v:/project/geopunt-plugins-qgis/geopunt4qgis.py#L37-L45)

All 7 dialogs are created in `__init__`, which loads API objects and models immediately, slowing QGIS startup. Instantiate dialogs lazily on first use instead.

---

### 12. `KEYS` file for API keys is not in the repo — no fallback or documentation
[`geopunt/basisregisters.py` L3–5](file:///v:/project/geopunt-plugins-qgis/geopunt/basisregisters.py#L3-L5)

There is `from .KEYS import KEYS` with no visible `KEYS.py` in the repo and no `KEYS.example.py` template. This will cause `ImportError` on fresh clones. Either:
- Ship a `KEYS.example.py` template, or  
- Move the key to the plugin settings dialog with a user-supplied input field.

---

### 13. `threading.Timer` used for marker cleanup — not Qt-thread-safe
[`geopunt4qgis.py` L271](file:///v:/project/geopunt-plugins-qgis/geopunt4qgis.py#L271)

```diff
- Timer( 3, self._clearGraphicLayer, ()).start()
+ QTimer.singleShot(3000, self._clearGraphicLayer)
```
`threading.Timer` callbacks run on a background thread; calling `scene().removeItem()` from a non-Qt thread can crash QGIS. Use `QTimer.singleShot` instead.

---

### 14. Bare `except:` in CSV loading
[`geopunt4QgisBatchGeoCode.py` L228](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisBatchGeoCode.py#L228)

```diff
- except:
+ except (IOError, UnicodeDecodeError) as e:
```
Bare excepts swallow keyboard interrupts and programming errors silently.

---

## 🟢 UX / Feature Suggestions

### 15. No progress feedback during batch geocoding
The batch validation loop (`validateRows`) in [`geopunt4QgisBatchGeoCode.py` L307](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisBatchGeoCode.py#L307) calls the API row-by-row synchronously. The `statusProgress` bar advances but `QApplication.processEvents()` is never called, so the UI stays frozen. Add `QApplication.processEvents()` calls or move to a `QgsTask`.

---

### 16. Elevation profile: y-axis label is hardcoded Dutch
[`geopunt4QgisElevation.py` L288–289](file:///v:/project/geopunt-plugins-qgis/geopunt4QgisElevation.py#L288-L289)

```diff
- self.ax.set_ylabel("hoogte (m)")
- self.ax.set_xlabel("afstand (%s)" % self.xscaleUnit[1] )
+ self.ax.set_ylabel(QCoreApplication.translate("geopunt4QgisElevationDialog", "hoogte (m)"))
+ self.ax.set_xlabel(QCoreApplication.translate("geopunt4QgisElevationDialog", "afstand (%s)") % self.xscaleUnit[1])
```
These strings bypass the i18n system.

---

### 17. No unit tests
The `testData/` directory exists but there are no automated tests. Consider adding `pytest-qgis` tests for:
- API wrapper classes in `geopunt/`
- geometry helper projection utilities in `tools/geometry.py`
- CSV parsing in the batch geocoder

---

### 18. Add "Export to clipboard" for reverse geocode result
When a reverse geocode returns an address, the user can only add it to a layer. A simple **"Copy to clipboard"** button in the message bar widget would be a low-effort, high-value addition.

---

## Summary Table

| # | File | Severity | Category |
|---|------|----------|----------|
| 1 | `tools/web.py` | 🔴 Critical | Bug |
| 2 | `geopunt4QgisSettingsdialog.py` | 🔴 Critical | Bug |
| 3 | `geopunt4QgisSettingsdialog.py` | 🔴 Critical | Bug |
| 4 | `geopunt4qgis.py` | 🔴 Critical | Bug/Compat |
| 5 | `geopunt/gipod.py` | 🔴 Critical | Bug |
| 6 | `geopunt/gipod.py` | 🟠 High | API |
| 7 | `tools/geometry.py` | 🟠 High | Compat |
| 8 | `tools/geometry.py` | 🟠 High | Compat |
| 9 | `tools/web.py` + dialogs | 🟠 High | Architecture |
| 10 | Multiple dialog files | 🟡 Medium | Code quality |
| 11 | `geopunt4qgis.py` | 🟡 Medium | Performance |
| 12 | `geopunt/basisregisters.py` | 🟡 Medium | DevEx |
| 13 | `geopunt4qgis.py` | 🟠 High | Crash risk |
| 14 | `geopunt4QgisBatchGeoCode.py` | 🟡 Medium | Code quality |
| 15 | `geopunt4QgisBatchGeoCode.py` | 🟡 Medium | UX |
| 16 | `geopunt4QgisElevation.py` | 🟡 Medium | i18n |
| 17 | (none) | 🟡 Medium | Testing |
| 18 | `geopunt4qgis.py` | 🟢 Low | Feature |
