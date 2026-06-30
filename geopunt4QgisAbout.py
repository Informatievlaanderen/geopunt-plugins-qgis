import os.path
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtWidgets import QDialog, QMessageBox 
from .ui_geopunt4QgisAbout import Ui_aboutDlg

PLUGIN_DIR= os.path.dirname(__file__)
class geopunt4QgisAboutDialog(QDialog):
    def __init__(self):
        super().__init__()

        # initialize locale
        locale = QSettings().value("locale/userLocale", "en")[:2]
        localePath = os.path.join(PLUGIN_DIR, 'i18n', 'geopunt4qgis_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)
            QCoreApplication.installTranslator(self.translator)
            
        if locale == 'en': 
            self.htmlFile = os.path.join(PLUGIN_DIR , 'i18n', 'about-en.html')
        else:
            self.htmlFile = os.path.join(PLUGIN_DIR, 'i18n', 'about-nl.html') 

        self._initGui()
    
    def _initGui(self):
        """Set up the user interface from Designer."""
        self.ui = Ui_aboutDlg() 
        self.ui.setupUi(self)
        with open(self.htmlFile,'r', encoding="utf-8") as html:
            self.ui.aboutText.setHtml( html.read() )

