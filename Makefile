#/***************************************************************************
# geopunt4Qgis
# 
# 'Makefile for geopunt4Qgis, a QGIS plugin'
#                             -------------------
#        begin                : 2013-12-05
#        copyright            : (C) 2013 by Kay Warrie
#        email                : kaywarrie@gmail.com
# ***************************************************************************/
# 
#/***************************************************************************
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU General Public License as published by  *
# *   the Free Software Foundation; either version 2 of the License, or     *
# *   (at your option) any later version.                                   *
# *                                                                         *
# ***************************************************************************/

# CONFIGURATION
PLUGIN_UPLOAD = $(CURDIR)/utils/plugin_upload.py

QGISDIR=.qgis2

# translation
SOURCES         = geopunt4qgis.py \
		  geopunt4QgisPoidialog.py \
		  geopunt4QgisAdresdialog.py \
		  geopunt4QgisAbout.py \
		  geopunt4QgisSettingsdialog.py \
		  geopunt4QgisBatchGeoCode.py \
		  geopunt4QgisGipod.py \
		  geopunt4QgisElevation.py \
		  geopunt4QgisDataCatalog.py \
		  geopunt4qgisParcel.py   \
		  versionChecker.py

FORMS           = ui_geopunt4qgis.ui \
		  ui_geopunt4QgisPoi.ui \
		  ui_geopunt4QgisAbout.ui \
		  ui_geopunt4QgisSettings.ui  \
		  ui_geopunt4QgisBatchGeoCode.ui \
		  ui_geopunt4QgisGIPOD.ui \
		  ui_geopunt4QgisElevation.ui \
		  ui_geopunt4QgisDataCatalog.ui \
		  ui_geopunt4qgisParcel.ui
		    
TRANSLATIONS = i18n/geopunt4qgis_en.ts i18n/geopunt4qgis_nl.ts

# plugin
PLUGINNAME = geopunt4Qgis

PY_FILES =  __init__.py geometryhelper.py geopunt.py \
geopunt4qgis.py geopunt4QgisAbout.py geopunt4qgisAdresdialog.py \
geopunt4QgisPoidialog.py geopunt4QgisSettingsdialog.py  \
geopunt4QgisBatchGeoCode.py batchGeoHelper.py reverseAdresMapTool.py \
geopunt4QgisGipod.py gipodHelper.py geopunt4qgisParcel.py \
geopunt4QgisElevation.py elevationHelper.py elevationProfileMapTool.py \
metadata.py geopunt4QgisDataCatalog.py versionChecker.py poiHelper.py \
parcelHelper.py

EXTRAS = images metadata.txt i18n/about-en.html i18n/about-nl.html ext-libs

UI_FILES = ui_geopunt4qgis.py ui_geopunt4QgisPoi.py ui_geopunt4QgisAbout.py \
ui_geopunt4QgisSettings.py ui_geopunt4QgisBatchGeoCode.py ui_geopunt4QgisGIPOD.py \
ui_geopunt4QgisElevation.py ui_geopunt4QgisDataCatalog.py ui_geopunt4qgisParcel.py

RESOURCE_FILES = resources_rc.py

default: compile

compile: $(UI_FILES) $(RESOURCE_FILES) 

%_rc.py : %.qrc
	pyrcc4 -o $*_rc.py  $<

%.py : %.ui
	pyuic4 -o $@ $<

# [KW]: extra command with my own python script, that I can also use on windows
# workflow testPlugin.py: pack -> extract at QGISDIR -> start QGIS
runplugin: compile transup 
	python $(CURDIR)/utils/testPlugin.py
	
# The deploy  target only works on unix like operating system where
# the Python plugin directory is located at: $HOME/$(QGISDIR)/python/plugins
# [KW]: use "make runplugin" instead on windows
deploy: compile transup 
	mkdir -p $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(PY_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(UI_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vf $(RESOURCE_FILES) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr $(EXTRAS) $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)
	cp -vfr i18n $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

# The dclean target removes compiled python files from plugin directory
# also delets any .svn entry
dclean:
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;

# The derase deletes deployed plugin
derase:
	rm -Rf $(HOME)/$(QGISDIR)/python/plugins/$(PLUGINNAME)

# The zip target deploys the plugin and creates a zip file with the deployed
# content. You can then upload the zip file on http://plugins.qgis.org
# [KW]: replaced by my own python script, that I can use on windows
# zip: deploy dclean 
# 	rm -f $(PLUGINNAME).zip
# 	cd $(HOME)/$(QGISDIR)/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)
zip:
	python $(CURDIR)/utils/packPlugin4upload.py


# Create a zip package of the plugin named $(PLUGINNAME).zip. 
# This requires use of git (your plugin development directory must be a 
# git repository).
# To use, pass a valid commit or tag as follows:
#   make package VERSION=v0.3
package: clean transclean dclean
		rm -f build/$(PLUGINNAME)-$(VERSION).zip
		git archive --prefix=$(PLUGINNAME)/ -o build/$(PLUGINNAME)-$(VERSION).zip $(VERSION)
		echo "Created package: $(PLUGINNAME)-$(VERSION).zip"

upload: zip
	$(PLUGIN_UPLOAD) build/$(PLUGINNAME).zip

# transup
# update .ts translation files, compile to .qm and .mk to .html
# [KW]: added custom compile_translations for html
transup: 
	pylupdate4 Makefile
	lrelease-qt4 i18n/*.ts
	utils/compile_html_translations.sh

# transclean
# deletes all .qm (form .ts) and html (from .mk) files
transclean:
	rm -f i18n/*.qm
	rm -f i18n/*.html

clean:
	rm $(UI_FILES) $(RESOURCE_FILES)

