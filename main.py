# -*- coding: utf-8 -*-
# PEP8:OK, LINT:OK, PY3:OK


#############################################################################
## This file may be used under the terms of the GNU General Public
## License version 2.0 or 3.0 as published by the Free Software Foundation
## and appearing in the file LICENSE.GPL included in the packaging of
## this file.  Please review the following information to ensure GNU
## General Public Licensing requirements will be met:
## http:#www.fsf.org/licensing/licenses/info/GPLv2.html and
## http:#www.gnu.org/copyleft/gpl.html.
##
## This file is provided AS IS with NO WARRANTY OF ANY KIND, INCLUDING THE
## WARRANTY OF DESIGN, MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
#############################################################################


# metadata
" Ninja .desktop file editor "
__version__ = ' 0.8 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 15/03/2013 '
__prj__ = ' dotdesktop '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import linesep, chmod
from getpass import getuser

from PyQt4.QtGui import (QLabel, QPushButton, QDoubleSpinBox, QFileDialog,
    QWidget, QScrollArea, QVBoxLayout, QComboBox, QLineEdit, QCheckBox, QColor,
    QDockWidget, QGraphicsDropShadowEffect, QGraphicsBlurEffect, QGroupBox,
    QMessageBox, QIcon)
from PyQt4.QtCore import QProcess

from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin


# constans
ACTIONS = '''

[Desktop Action Name_Your_Command_here]
Name=Name_Your_Command_here
Exec=Your_Command_here
OnlyShowIn=Unity;

'''


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        super(Main, self).initialize(*args, **kwargs)
        self.chooser, self.process = QComboBox(), QProcess()
        self.chooser.addItems([' Ubuntu Unity QuickList .desktop ',
                               ' KDE Plasma MetaData .desktop ',
                               ' FreeDesktop Standard .desktop '])
        self.chooser.currentIndexChanged.connect(self.on_index_changed)
        self.chooser.setToolTip('Select a target .desktop file format')

        # Standard FreeDesktop
        self.group1 = QGroupBox()
        self.group1.setTitle(' Standard ')
        self.ledVersion, self.ledCategories = QDoubleSpinBox(), QComboBox()
        self.ledVersion.setMinimum(0.1)
        self.ledVersion.setMaximum(999.9)
        self.ledVersion.setValue(1.0)
        self.ledVersion.setDecimals(1)
        self.ledType, self.ledName = QLineEdit('Application'), QLineEdit('App')
        self.ledGenericName = QLineEdit('Generic App')
        self.ledComment, self.ledIcon = QLineEdit('App'), QLineEdit('icon.svg')
        self.ledCategories.addItems(['Python Programming Language',
            'Development', 'Ruby', 'C++', 'Amateur Radio', 'Communication',
            'Cross Platform', 'Databases', 'Debug', 'Documentation', 'Editors',
            'Education', 'Electronics', 'Email', 'Embebed Devices', 'Fonts',
            'GNOME Desktop Environment', 'GNU R Statistical System',
            'GObject Introspection Data', 'Games and Amusement',
            'Gnustep Desktop Environtment', 'Graphics',
            'Haskell Programming Language',
            'Internationalization and Localization', 'Internet',
            'Interpreted Computer Languages', 'KDE Software Compilation',
            'Kernel and Modules', 'Libraries', 'Libraries - Development',
            'Libraries - Old', 'Lisp Programming Language', 'Localization',
            'Mathematics', 'Meta Packages', 'Miscelaneous - Graphical',
            'Miscelaneous - Text Based', 'Mono/CLI Infraestructure',
            'Multimedia', 'Networking', 'Newsgroups',
            'OCaml Programming Language', 'PHP Programming Language',
            'Perl Programming Language', 'Ruby Programming Language',
            'Science', 'Shells', 'System Administration', 'TeX Authoring',
            'Utilities', 'Version Control Systems', 'Video Software',
            'Web Servers', 'Word Processing', 'Xfce Desktop Environment',
            'Zope/Plone Environment'])

        self.ledExec, self.ledTryExec = QLineEdit('myapp'), QLineEdit('myapp')
        self.ledMymeType = QLineEdit('application/x-desktop')
        self.ledTerminal = QComboBox()
        self.ledTerminal.addItems(['False', 'True'])
        self.ledActions = QLineEdit('Next;Previous')
        self.ledOnlyShowIn = QLineEdit('Unity;KDE')
        self.ledNotShowIn = QLineEdit('Gnome2')
        vboxg1 = QVBoxLayout(self.group1)
        for each_widget in (QLabel('Version'), self.ledVersion, QLabel('Type'),
            self.ledType, QLabel('Name'), self.ledName, QLabel('GenericName'),
            self.ledGenericName, QLabel('Comment'), self.ledComment,
            QLabel('Icon'), self.ledIcon, QLabel('Categories'),
            self.ledCategories, QLabel('Exec'), self.ledExec, QLabel('TryExec'),
            self.ledTryExec, QLabel('MymeType'), self.ledMymeType,
            QLabel('Terminal'), self.ledTerminal, QLabel('Actions'),
            self.ledActions, QLabel('OnlyShowIn'), self.ledOnlyShowIn,
            QLabel('NotShowIn'), self.ledNotShowIn):
            vboxg1.addWidget(each_widget)

        # KDE Plasma
        self.group2 = QGroupBox()
        self.group2.setTitle(' KDE Plasma ')
        self.group2.setGraphicsEffect(QGraphicsBlurEffect(self))
        self.ledEncoding, self.ledXPlasmaAPI = QComboBox(), QComboBox()
        self.ledEncoding.addItems(['UTF-8', 'ISO-8859-1'])
        self.ledServiceType = QLineEdit('Plasma/Applet')
        self.ledXPlasmaAPI.addItems([
                        'Python', 'Javascript', 'Ruby', 'C++', 'HTML5', 'QML'])
        self.ledXPlasmaMainScript = QLineEdit('path/to/your/code.py')
        self.ledXKDEPluginInfoAuthor = QLineEdit(getuser())
        self.ledXKDEPluginInfoEmail = QLineEdit(getuser() + '@gmail.com')
        self.ledXKDEPluginInfoName = QLineEdit('Hello-World')
        self.ledXKDEPluginInfoVersion = QLineEdit('1.0')
        self.ledXKDEPluginInfoWebsite = QLineEdit('http:plasma.kde.org')
        self.ledXKDEPluginInfoCategory = QComboBox()
        self.ledXKDEPluginInfoCategory.addItems(['Application Launchers',
            'Accessibility', 'Astronomy', 'Date and Time',
            'Development Tools', 'Education', 'Environment', 'Examples',
            'File System', 'Fun and Games', 'Graphics', 'Language', 'Mapping',
            'Multimedia', 'Online Services', 'System Information', 'Utilities',
            'Windows and Tasks', 'Miscelaneous'])
        self.ledXKDEPluginInfoDepends = QLineEdit()
        self.ledXKDEPluginInfoLicense = QLineEdit('GPL')
        self.ledXKDEPluginInfoEnabledByDefault = QComboBox()
        self.ledXKDEPluginInfoEnabledByDefault.addItems(['True', 'False'])
        vboxg2 = QVBoxLayout(self.group2)
        for each_widget in (
            QLabel('Encoding'), self.ledEncoding,
            QLabel('ServiceType'), self.ledServiceType,
            QLabel('X-Plasma-API'), self.ledXPlasmaAPI,
            QLabel('X-Plasma-MainScript'), self.ledXPlasmaMainScript,
            QLabel('X-KDE-PluginInfo-Author'), self.ledXKDEPluginInfoAuthor,
            QLabel('X-KDE-PluginInfo-Email'), self.ledXKDEPluginInfoEmail,
            QLabel('X-KDE-PluginInfo-Name'), self.ledXKDEPluginInfoName,
            QLabel('X-KDE-PluginInfo-Version'), self.ledXKDEPluginInfoVersion,
            QLabel('X-KDE-PluginInfo-Website'), self.ledXKDEPluginInfoWebsite,
            QLabel('X-KDE-PluginInfo-Category'), self.ledXKDEPluginInfoCategory,
            QLabel('X-KDE-PluginInfo-Depends'), self.ledXKDEPluginInfoDepends,
            QLabel('X-KDE-PluginInfo-License'), self.ledXKDEPluginInfoLicense,
            QLabel('X-KDE-PluginInfo-EnabledByDefault'),
            self.ledXKDEPluginInfoEnabledByDefault):
            vboxg2.addWidget(each_widget)

        # Ubuntu Unity
        self.ledXAyatanaDesktopShortcuts = QLineEdit('Next;Previous')

        self.checkbox1 = QCheckBox('Open .desktop file when done')
        self.checkbox2 = QCheckBox('Make .desktop file Executable')
        [a.setChecked(True) for a in (self.checkbox1, self.checkbox2)]

        self.button = QPushButton(' Make .Desktop File ! ')
        self.button.setMinimumSize(100, 50)
        self.button.clicked.connect(self.writeFile)
        glow = QGraphicsDropShadowEffect(self)
        glow.setOffset(0)
        glow.setBlurRadius(99)
        glow.setColor(QColor(99, 255, 255))
        self.button.setGraphicsEffect(glow)
        glow.setEnabled(True)

        class TransientWidget(QWidget):
            ' persistant widget thingy '
            def __init__(self, widget_list):
                ' init sub class '
                super(TransientWidget, self).__init__()
                vbox = QVBoxLayout(self)
                for each_widget in widget_list:
                    vbox.addWidget(each_widget)

        tw = TransientWidget((self.chooser, self.group1, self.group2,
            QLabel('X-Ayatana-Desktop-Shortcuts'),
            self.ledXAyatanaDesktopShortcuts, QLabel(''),
            self.checkbox1, self.checkbox2, self.button))
        self.dock, self.scrollable = QDockWidget(), QScrollArea()
        self.scrollable.setWidgetResizable(True)
        self.scrollable.setWidget(tw)
        self.dock.setWindowTitle(__doc__)
        self.dock.setStyleSheet('QDockWidget::title{text-align: center;}')
        self.dock.setWidget(self.scrollable)
        ExplorerContainer().addTab(self.dock, "DotDesktop")
        QPushButton(QIcon.fromTheme("help-about"), 'About', self.dock
          ).clicked.connect(lambda: QMessageBox.information(self.dock, __doc__,
          ''.join((__doc__, __version__, __license__, 'by', __author__))))

    def writeFile(self):
        ' write the .desktop file to disk '

        UNITY = ''.join(a for a in iter((
        'OnlyShowIn=', str(self.ledOnlyShowIn.text()), linesep,
        'NotShowIn=', str(self.ledNotShowIn.text()), linesep,
        'X-Ayatana-Desktop-Shortcuts=',
        str(self.ledXAyatanaDesktopShortcuts.text()), linesep)))

        PLASMA = ''.join(a for a in iter((
        'OnlyShowIn=', str(self.ledOnlyShowIn.text()), linesep,
        'NotShowIn=', str(self.ledNotShowIn.text()), linesep,
        'Encoding=', str(self.ledEncoding.currentText()), linesep,
        'ServiceTypes=', str(self.ledServiceType.text()), linesep,
        'X-Plasma-API=', str(self.ledXPlasmaAPI.currentText()), linesep,
        'X-Plasma-MainScript=', str(self.ledXPlasmaMainScript.text()), linesep,
        'X-KDE-PluginInfo-Author=', str(self.ledXKDEPluginInfoAuthor.text()),
        linesep,
        'X-KDE-PluginInfo-Email=', str(self.ledXKDEPluginInfoEmail.text()),
        linesep,
        'X-KDE-PluginInfo-Name=', str(self.ledXKDEPluginInfoName.text()),
        linesep,
        'X-KDE-PluginInfo-Version=', str(self.ledXKDEPluginInfoVersion.text()),
        linesep,
        'X-KDE-PluginInfo-Website=', str(self.ledXKDEPluginInfoWebsite.text()),
        linesep,
        'X-KDE-PluginInfo-Category=',
        str(self.ledXKDEPluginInfoCategory.currentText()), linesep,
        'X-KDE-PluginInfo-Depends=', str(self.ledXKDEPluginInfoDepends.text()),
        linesep,
        'X-KDE-PluginInfo-License=', str(self.ledXKDEPluginInfoLicense.text()),
        linesep,
        'X-KDE-PluginInfo-EnabledByDefault=',
        str(self.ledXKDEPluginInfoEnabledByDefault.currentText()), linesep)))

        BASE = ''.join(a for a in iter((
        '[Desktop Entry]', linesep,
        'Version=', str(self.ledVersion.value()), linesep,
        'Type=', str(self.ledType.text()), linesep,
        'Name=', str(self.ledName.text()), linesep,
        'Comment=', str(self.ledComment.text()), linesep,
        'TryExec=', str(self.ledTryExec.text()), linesep,
        'Exec=', str(self.ledExec.text()), linesep,
        'Icon=', str(self.ledIcon.text()), linesep,
        'MimeType=', str(self.ledMymeType.text()), linesep,
        'Actions=', str(self.ledActions.text()), linesep,
        'Terminal=', str(self.ledTerminal.currentText()), linesep)))

        ACTIONS * len(str(self.ledActions.text()).lower().strip().split(';'))

        fnm = str(QFileDialog.getSaveFileName(self.dock, '', '', "(*.desktop)"))
        with open(fnm, 'w') as f:
            if self.chooser.currentIndex() is 0 and fnm is not '':
                f.write(''.join(a for a in iter((BASE, UNITY, ACTIONS))))
            elif self.chooser.currentIndex() is 1 and fnm is not '':
                f.write(''.join(a for a in iter((BASE, PLASMA))))
            elif fnm is not '':
                f.write(BASE)

        if self.checkbox2.isChecked() and fnm is not '':
            try:
                chmod(fnm, 0775)  # Py2
            except:
                chmod(fnm, 0o775)  # Py3

        if self.checkbox1.isChecked() and fnm is not '':
            self.process.start('ninja-ide ' + fnm)
            if not self.process.waitForStarted():
                print((" ERROR: FAIL: {} failed!".format(fnm)))
                return

    def on_index_changed(self):
        ' enable disable the qgroupbox if needed '
        if self.chooser.currentIndex() is 1:
            self.group2.graphicsEffect().setEnabled(False)
            self.group2.setEnabled(True)
        else:
            self.group2.graphicsEffect().setEnabled(True)
            self.group2.setEnabled(False)
        if self.chooser.currentIndex() is 0:
            self.ledXAyatanaDesktopShortcuts.setEnabled(True)
        else:
            self.ledXAyatanaDesktopShortcuts.setEnabled(False)


###############################################################################


if __name__ == "__main__":
    print(__doc__)
