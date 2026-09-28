
Test results for QGIS4 plugin (geopunt4Qgis) supplied by customers of the Flemish government
====================================================================

> **All tests performed in EPSG:3812 (standard). Some cross-CRS-checked
> with EPSG:31370, 4326 & 3857.**

1. **Plugin disable en re-enable (zonder restart QGIS)**

    a.  Disable the plug-in via the plug-in manager
    b.  Check the menu (Web \> plugin \> ...)
    c.  Buttons are still there:
        ![](./img/media/image1.png){width="4.100355424321959in"
        height="2.8835826771653545in"}
    d.  Re-enable the plugin. Check the menu again.
    e.  Buttons are now double:
        ![](./img/media/image2.png){width="4.042016622922135in"
        height="5.067106299212599in"}
    f.  Restarting QGIS fixes this.

    --> FIXED, the plugin now disables the menu when the plugin is disabled.

2. **Address**

    a.  Address dialog panel shows empty field?
        ![](./img/media/image3.png){width="4.661194225721784in"
        height="2.9606714785651795in"}
    b.  Not sure if this is used somewhere.

    --> FIXED, removed

3. **Address**

    a.  Search for a specific address with house number (eg "Gent" \>
        "Korenmarkt 10").
    b.  Double-click a result, or use \"zoom naar\".
    c.  Map only does the panning, not zooming.
    d.  Same issue in EPSG:4326, 3857, 31370
    e.  Note: when using only the street, [without]{.underline} house
        number (eg "Gent" \> "Korenmarkt"), zooming does work.

    --> FIXED: when a single address is returned (no bounding box or empty bounding box), the map zooms and pans to the location at scale 1:1000.

4. **Address**

    a.  Switch the address layer from memory to a permanent file
        (GeoPackage) with a custom name and folder.
    b.  Click \"Toevoegen aan kaart\" for another result.
    c.  Python error, address is not added:
        ```
            2026-08-21T09:56:12     WARNING    Traceback (most recent
            call last):\

                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\geopunt4QgisAdresdialog.py\",
            line 137, in onAdd2mapKnopClick\
                          self.\_addToMap(item.text())\
                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\geopunt4QgisAdresdialog.py\",
            line 189, in \_addToMap\
                          self.gh.save_adres_point( pt, adres,
            typeAddress=LocationType,\
                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\tools\\geometry.py\",
            line 177, in save_adres_point\
                          self.adresProvider.addFeatures(\[fet\])\
                         RuntimeError: wrapped C/C++ object of type
            QgsVectorDataProvider has been deleted
        ```
    --> FIXED: `geometryHelper.save_adres_point` (tools/geometry.py) no longer trusts a cached `QgsVectorDataProvider` blindly. Before writing it now verifies the provider is still valid (`isSourceValid()`) and that the layer is still loaded; when the source switches from memory to a permanent file the memory layer is exported and the file layer's provider is used, so a dangling `QgsVectorDataProvider` can never be passed to `addFeatures` anymore.

5. **Address:**

    a.  Toggle \"search on Enter\" instead of \"search on edit\" in
        Settings.
    b.  Address dialog doesn't respect it (still live search while
        typing).

    --> FIXED: this setting was obsolete, the search is now always on edit as service is now more responsive then in the past.
    --> FIXED: the setting has been removed from the settings dialog. TODO

6. **Reverse geocoding:**

    a.  \"Prik een adres op de kaart\", same Python error as 3.c

    --> FIXED: uses the same `geometryHelper.save_adres_point` path, so the permanent-file switch is now handled (see item 4 for details).

7. **Reverse geocoding:**

    a.  Mouse is stuck at the \"Prik een adres op de kaart\" tool.
    b.  Have to click other QGIS tool (e.g. pan map) to get "out" of the
        reverse geocoding tool.

    --> NOERROR: Tested, mouse not stuck, the tool is still active until the user clicks another tool. This is the expected behavior. It is possible to change this behavior, but it is not a bug. 

8. **Reverse geocoding:**

    a.  Click outside Flanders (sea, France, Netherlands).
    b.  Python error instead of a warning message. Yellow square symbols
        don't dissappear:
        ![](./img/media/image4.png){width="5.33379593175853in"
        height="2.58752624671916in"}
    c.  Same issue in EPSG:4326, 3857, 31370

    --> FIXED: Better warning message is now shown.

9. **Batch geocoding**

    a.  Open the batch dialog, browse to **addresses_columns.csv**, set
        separator = comma, encoding = UTF-8.
    b.  column-mapping controls not working:
        ![](./img/media/image5.png){width="5.721580271216098in"
        height="5.108554243219597in"}

    --> FIXED

10. **POI**

    a.  Search for POI's.
    b.  Double-click a result, or use \"zoom naar\".
    c.  Map only does the panning, not zooming. (Same bug as 2.c)

    --> FIXED: when a single POI is returned, the map zooms and pans to the location at scale 1:1000.

11. **POI**

    a.  Search for POI's with \> 32 results
    b.  Results "Getoond" en "Gevonden" stuck at 32 max (there are more
        then 32 schools):
        ![](./img/media/image6.png){width="4.748799212598425in"
        height="4.724195100612423in"}

    --> NOERROR: this the preview based on the first 32 results, but the total number of results is shown in the status bar (see below). The add button wiill add all results to the map, not only the first 32.

12. **Elevation:**

    a.  Line-draw tool not showing the line while drawing.

    --> FIXED, a blue line is now shown while drawing, the line already drawn remains red.

13. **Elevation:**

    a.  Refresh profile: missing button text:
        ![](./img/media/image7.png){width="3.5938527996500436in"
        height="2.8158541119860017in"}

    --> FIXED: Done, added icon to the button

14. **Elevation:**

    a.  A line drawn (partly or completely) outside Flanders / over
        water where DHM has no data gives Python error (instead of
        generic message that data isn't available):

        ```
        Traceback (most recent call last):\
                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\mapTools\\elevationProfile.py\",
            line 41, in canvasDoubleClickEvent\
                          self.callback( self.rubberBand )\
                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\geopunt4QgisElevation.py\",
            line 301, in maptoolCallBack\
                          self.plot()\
                          File
            \"C:\\Users/HendrikMeersman/AppData/Roaming/QGIS/QGIS4\\profiles\\default/python/plugins\\geopunt4Qgis\\geopunt4QgisElevation.py\",
            line 277, in plot\
                          ymin = np.min( \[n\[3\] for n in self.profile
            if n\[3\] \> -9999 \] )\
                          \^\^\^\^\^\^\^\^\^\^\^\^\
                         TypeError: \'\>\' not supported between
            instances of \'NoneType\' and \'int\'
        ```
    --> FIXED: Done, a better warning message is now shown when the profile contains no valid data.

15. **Datavindplaats:**

    a.  Buttons for "previous" and "next" page with results are missing
        labels:
        ![](./img/media/image8.png){width="4.350377296587927in"
        height="0.883409886264217in"}

    -->  FIXED: Done, added icons to the buttons

16. **Settings dialog:**

    a.  Toggle the GIPOD checkbox to a state that differs from the
        current POI checkbox (e.g. "Save to [file]{.underline}" for POI
        and "Save to [temporary layer]{.underline}" for GIPOD).
    b.  Save, close QGIS entirely, then reopen Settings.
    c.  Checkboxes for GIPOD and POI are the same state again.

    --> FIXED: POI tool saving is fixed.
    --> FIXED: Gipod has been removed from the plugin, so this is no longer relevant.
    --> FIXED: I have now also removed the Gipod entry in the settings dialog

17. **Static code review with AI — `geopunt4Qgis` and dependencies**

    Source code review of the batch geocoding dialog and its dependency
    chain (`tools/batchGeo.py`, `tools/geometry.py`, `tools/web.py`,
    `tools/settings.py`, `mapTools/reverseAdres.py`,
    `geopunt/basisregisters.py`). Sorted by severity.

    **Critical / correctness bugs**

    17.1  `tools/web.py:39` — `sys.exc_info` is not called. The f-string
        interpolates the function object, so the raised message contains
        `<built-in function exc_info ...>` instead of the exception triple.
        Needs `sys.exc_info()`. FIXED

    17.2  `geopunt4QgisBatchGeoCode.py:237` — `next(csvReader)` on an empty
        CSV raises an uncaught `StopIteration`. Wrap in
        `try/except StopIteration`. FIXED

    17.3  `geopunt4QgisBatchGeoCode.py:272` — `line[col]` raises
        `IndexError` on any data row with fewer fields than the header.
        Use a length check or a default value. NOW:
        `val = line[col] if col < len(line) else ""`. FIXED

    17.4  `geopunt4QgisBatchGeoCode.py:18` and :403 —
        `root.find('.//{...}pos').text` returns `None` when the GML has no
        `<pos>` element, and `.split()` then crashes. Guard with a
        `None` check. FIXED: `_gmlpointToXY` now returns `None` when the
        `<pos>` element is missing, its caller skips the row, and the
        second parse site (line ~485) skips when `pos_text` is `None`.

    17.5  `geopunt4QgisBatchGeoCode.py:426` — malformed `QFileDialog` filter:
        `"Comma separated value File (*.csv) (*.csv)"` duplicates the
        `(*.ext)` part that belongs to the description only. Compare the
        correct syntax in `tools/batchGeo.py:98`. FIXED: filter now reads
        `"Comma separated value File (*.csv);;Text Files (*.txt);;Any File (*.*)"`.

    17.6  `geopunt4QgisBatchGeoCode.py:225` — the CSV file handle opened via
        `open(...)` inside `csv.reader(...)` is never closed. Use a context
        manager or close in a `finally` block. FIXED: call site now reads
        `with open(self.csv, 'r', encoding=enc, newline='') as f:` (line 232).

    **QGIS 4 API deprecations (plugin targets QGIS 4.00–4.99)**

    17.7  `tools/batchGeo.py:79`, `tools/geometry.py:207`,
        `tools/poi.py:115,245`, `tools/parcel.py:62`,
        `tools/elevation.py:57,110` — `QgsVectorFileWriter.writeAsVectorFormat`
        is deprecated; migrate to `writeAsVectorFormatV3()` /
        `QgsVectorFileWriter.create()`. Already flagged in
        `docs/plugin_analysis.md:88`. FIXED

    17.8  `tools/web.py` — `QgsBlockingNetworkRequest` is a legacy API; the
        modern idiom is `QgsNetworkAccessManager` (non-blocking
        `fetch_non_blocking` already exists in the same file but is not used
        by `adresMatch`). TODO

    **Code-smell / consistency**

    17.9 `tools/batchGeo.py:119-122` — dead code, a duplicate CSV branch
        that is unreachable because lines 117-118 match first. TODO

    17.10 `tools/settings.py:11` and `geopunt4QgisSettingsdialog.py:71,74,156`
        — key typo `proxyOverwiteEnabled` (should be `proxyOverwriteEnabled`).
        Consistent on read and write, so no functional impact. TODO

    17.11 `geopunt4QgisBatchGeoCode.py:449-451` — `clean()` clears
        `adresColSelect`, `huisnrSelect` and `gemeenteColSelect` but not
        `pcColSelect`, inconsistent with the `loadTable` reset at line 200.
        TODO

    17.12 `geopunt/basisregisters.py:51,81` — `except BaseException` swallows
        `KeyboardInterrupt`/`SystemExit`; should be `except Exception`. TODO

    17.13 `tools/batchGeo.py:37` — `QgsVectorLayer("Point", ...)` has no CRS
        (defaults to EPSG:4326) while `tools/geometry.py:182` explicitly uses
        `Point?crs=epsg:31370`; inconsistent with the rest of the plugin. TODO

    17.14 `tools/geometry.py:146-152` (`zoomtoRec`) — `setExtent`/`refresh`
        called unconditionally, then again in the `else` branch (redundant).
        TODO

    17.15 `geopunt4QgisBatchGeoCode.py:86` — `webbrowser.open_new_tab(...)`
        works, but `QDesktopServices.openUrl(QUrl(...))` is idiomatic PyQt.
        TODO

    17.16 `geopunt4QgisBatchGeoCode.py:98` — `self.proxy` is read from
        `settings()` but never passed to the API layer (`adresMatch` →
        `web.getUrlData`), so the configured proxy is silently ignored. TODO

    17.17 `geopunt4QgisBatchGeoCode.py:366,370` — `setEnabled(0)` /
        `addItem("")`: `setEnabled(False)` and a `<geen>` placeholder are
        more idiomatic. TODO

    17.18 `mapTools/reverseAdres.py` — no `keyPressEvent` for `Esc` to cancel
        the picking tool (minor UX). TODO
