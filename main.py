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
" Ninja-IDE .desktop file editor "
__version__ = ' 0.4 '
__license__ = ' GPL '
__author__ = ' juancarlospaco '
__email__ = ' juancarlospaco@ubuntu.com '
__url__ = ''
__date__ = ' 30/05/2013 '
__prj__ = ' dotdesktop '
__docformat__ = 'html'
__source__ = ''
__full_licence__ = ''


# imports
from os import path, linesep, chmod
from getpass import getuser
from sip import setapi

from PyQt4.QtGui import (QLabel, QPushButton, QDoubleSpinBox, QFileDialog,
    QWidget, QScrollArea, QVBoxLayout, QComboBox, QCursor, QLineEdit, QCheckBox)

from PyQt4.QtCore import Qt, QProcess

from ninja_ide.gui.explorer.explorer_container import ExplorerContainer
from ninja_ide.core import plugin


# API 2
(setapi(a, 2) for a in ("QDate", "QDateTime", "QString", "QTime", "QUrl",
                        "QTextStream", "QVariant"))


# constans


###############################################################################


class Main(plugin.Plugin):
    " Main Class "
    def initialize(self, *args, **kwargs):
        " Init Main Class "
        ec = ExplorerContainer()
        super(Main, self).initialize(*args, **kwargs)
        self.titlelbl = QLabel('<center><h3>{}</h3></center>'.format(__doc__))
        self.chooser = QComboBox()
        self.chooser.setCursor(QCursor(Qt.PointingHandCursor))
        self.chooser.addItems([' Ubuntu Unity QuickList .desktop ',
                               ' KDE Plasma MetaData .desktop ',
                               ' FreeDesktop Standard .desktop '])
        self.chooser.setToolTip('Select a target .desktop file format')

        self.process = QProcess()
        self.process.finished.connect(self.processFinished)

        # Standard FreeDesktop
        self.lblVersion = QLabel('Version')
        self.ledVersion = QDoubleSpinBox()
        self.ledVersion.setMinimum(0.1)
        self.ledVersion.setMaximum(999.9)
        self.ledVersion.setValue(1.0)
        self.ledVersion.setDecimals(1)

        self.lblType = QLabel('Type')
        self.ledType = QLineEdit('Application')

        self.lblName = QLabel('Name')
        self.ledName = QLineEdit('My App')

        self.lblGenericName = QLabel('GenericName')
        self.ledGenericName = QLineEdit('Generic App')

        self.lblComment = QLabel('Comment')
        self.ledComment = QLineEdit('Just Another App')

        self.lblIcon = QLabel('Icon')
        self.ledIcon = QLineEdit('/path/to/icon.svg')

        self.lblCategories = QLabel('Categories')
        self.ledCategories = QComboBox()
        self.ledCategories.addItems(['Python Programming Language',
            'Development', 'Ruby', 'C++',
            'Amateur Radio', 'Communication', 'Cross Platform', 'Databases',
            'Debug', 'Documentation', 'Editors', 'Education', 'Electronics',
            'Email', 'Embebed Devices', 'Fonts', 'GNOME Desktop Environment',
            'GNU R Statistical System', 'GObject Introspection Data',
            'Games and Amusement', 'Gnustep Desktop Environtment', 'Graphics',
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
            'Zope/Plone Environment'
        ])

        self.lblExec = QLabel('Exec')
        self.ledExec = QLineEdit('myexecutable --parameters')

        self.lblTryExec = QLabel('TryExec')
        self.ledTryExec = QLineEdit('myexecutable --parameters')

        self.lblMymeType = QLabel('MymeType')
        self.ledMymeType = QLineEdit('application/x-desktop')

        self.lblTerminal = QLabel('Terminal')
        self.ledTerminal = QComboBox()
        self.ledTerminal.addItems(['False', 'True'])

        self.lblActions = QLabel('Actions')
        self.ledActions = QLineEdit('Next;Previous')

        self.lblOnlyShowIn = QLabel('OnlyShowIn')
        self.ledOnlyShowIn = QLineEdit('Unity;KDE')

        self.lblNotShowIn = QLabel('NotShowIn')
        self.ledNotShowIn = QLineEdit('Gnome2')

        # KDE Plasma
        self.lblEncoding = QLabel('Encoding')
        self.ledEncoding = QComboBox()
        self.ledEncoding.addItems(['UTF-8', 'ISO-8859-1'])

        self.lblServiceType = QLabel('ServiceType')
        self.ledServiceType = QLineEdit('Plasma/Applet')

        self.lblXPlasmaAPI = QLabel('X-Plasma-API')
        self.ledXPlasmaAPI = QComboBox()
        self.ledXPlasmaAPI.addItems([
                        'Python', 'Javascript', 'Ruby', 'C++', 'HTML5', 'QML'])

        self.lblXPlasmaMainScript = QLabel('X-Plasma-MainScript')
        self.ledXPlasmaMainScript = QLineEdit('path/to/your/code.py')

        self.lblXKDEPluginInfoAuthor = QLabel('X-KDE-PluginInfo-Author')
        self.ledXKDEPluginInfoAuthor = QLineEdit(getuser())

        self.lblXKDEPluginInfoEmail = QLabel('X-KDE-PluginInfo-Email')
        self.ledXKDEPluginInfoEmail = QLineEdit(getuser() + '@gmail.com')

        self.lblXKDEPluginInfoName = QLabel('X-KDE-PluginInfo-Name')
        self.ledXKDEPluginInfoName = QLineEdit('Hello-World')

        self.lblXKDEPluginInfoVersion = QLabel('X-KDE-PluginInfo-Version')
        self.ledXKDEPluginInfoVersion = QLineEdit('1.0')

        self.lblXKDEPluginInfoWebsite = QLabel('X-KDE-PluginInfo-Website')
        self.ledXKDEPluginInfoWebsite = QLineEdit('http:plasma.kde.org')

        self.lblXKDEPluginInfoCategory = QLabel('X-KDE-PluginInfo-Category')
        self.ledXKDEPluginInfoCategory = QComboBox()
        self.ledXKDEPluginInfoCategory.addItems(['Application Launchers',
            'Accessibility', 'Astronomy', 'Date and Time',
            'Development Tools', 'Education', 'Environment', 'Examples',
            'File System', 'Fun and Games', 'Graphics', 'Language', 'Mapping',
            'Multimedia', 'Online Services', 'System Information', 'Utilities',
            'Windows and Tasks', 'Miscelaneous'])

        self.lblXKDEPluginInfoDepends = QLabel('X-KDE-PluginInfo-Depends')
        self.ledXKDEPluginInfoDepends = QLineEdit('')

        self.lblXKDEPluginInfoLicense = QLabel('X-KDE-PluginInfo-License')
        self.ledXKDEPluginInfoLicense = QLineEdit('GPL')

        self.lblXKDEPluginInfoEnabledByDefault = QLabel(
                                        'X-KDE-PluginInfo-EnabledByDefault')
        self.ledXKDEPluginInfoEnabledByDefault = QComboBox()
        self.ledXKDEPluginInfoEnabledByDefault.addItems(['True', 'False'])

        # Ubuntu Unity
        self.lblXAyatanaDesktopShortcuts = QLabel('X-Ayatana-Desktop-Shortcuts')
        self.ledXAyatanaDesktopShortcuts = QLineEdit('Next;Previous')

        self.optionlbl = QLabel('        Open .desktop file when done')
        self.checkbox1 = QCheckBox(self.optionlbl)
        self.checkbox1.setChecked(True)

        self.permislbl = QLabel('        Make .desktop file Executable')
        self.checkbox2 = QCheckBox(self.permislbl)

        self.button = QPushButton(' OK ! ')
        self.button.clicked.connect(self.writeFile)
        self.button.setCursor(QCursor(Qt.PointingHandCursor))
        self.button.setToolTip(' Make the .desktop file ! ')

        class TransientWidget(QWidget):
            ' persistant widget thingy '
            def __init__(self, widget_list):
                ' init sub class '
                super(TransientWidget, self).__init__()
                vbox = QVBoxLayout(self)
                for each_widget in widget_list:
                    vbox.addWidget(each_widget)

        tw = TransientWidget((
            self.titlelbl, self.chooser, QLabel(''),
            self.lblVersion, self.ledVersion,
            self.lblType, self.ledType,
            self.lblName, self.ledName,
            self.lblGenericName, self.ledGenericName,
            self.lblComment, self.ledComment,
            self.lblIcon, self.ledIcon,
            self.lblCategories, self.ledCategories,
            self.lblExec, self.ledExec,
            self.lblTryExec, self.ledTryExec,
            self.lblMymeType, self.ledMymeType,
            self.lblTerminal, self.ledTerminal,
            self.lblActions, self.ledActions,
            self.lblOnlyShowIn, self.ledOnlyShowIn,
            self.lblNotShowIn, self.ledNotShowIn, QLabel(''),
            self.lblEncoding, self.ledEncoding,
            self.lblServiceType, self.ledServiceType,
            self.lblXPlasmaAPI, self.ledXPlasmaAPI,
            self.lblXPlasmaMainScript, self.ledXPlasmaMainScript,
            self.lblXKDEPluginInfoAuthor, self.ledXKDEPluginInfoAuthor,
            self.lblXKDEPluginInfoEmail, self.ledXKDEPluginInfoEmail,
            self.lblXKDEPluginInfoName, self.ledXKDEPluginInfoName,
            self.lblXKDEPluginInfoVersion, self.ledXKDEPluginInfoVersion,
            self.lblXKDEPluginInfoWebsite, self.ledXKDEPluginInfoWebsite,
            self.lblXKDEPluginInfoCategory, self.ledXKDEPluginInfoCategory,
            self.lblXKDEPluginInfoDepends, self.ledXKDEPluginInfoDepends,
            self.lblXKDEPluginInfoLicense, self.ledXKDEPluginInfoLicense,
            self.lblXKDEPluginInfoEnabledByDefault,
            self.ledXKDEPluginInfoEnabledByDefault,
            QLabel(''),
            self.lblXAyatanaDesktopShortcuts, self.ledXAyatanaDesktopShortcuts,
            QLabel(''),
            self.optionlbl,
            self.permislbl,
            QLabel(''),
            self.button
        ))
        self.scrollable = QScrollArea()
        self.scrollable.setWidget(tw)
        ec.addTab(self.scrollable, "DotDesktop")

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
            'X-Plasma-MainScript=', str(self.ledXPlasmaMainScript.text()),
            linesep,
            'X-KDE-PluginInfo-Author=',
            str(self.ledXKDEPluginInfoAuthor.text()),
            linesep,
            'X-KDE-PluginInfo-Email=', str(self.ledXKDEPluginInfoEmail.text()),
            linesep,
            'X-KDE-PluginInfo-Name=', str(self.ledXKDEPluginInfoName.text()),
            linesep,
            'X-KDE-PluginInfo-Version=',
            str(self.ledXKDEPluginInfoVersion.text()),
            linesep,
            'X-KDE-PluginInfo-Website=',
            str(self.ledXKDEPluginInfoWebsite.text()),
            linesep,
            'X-KDE-PluginInfo-Category=',
            str(self.ledXKDEPluginInfoCategory.currentText()),
            linesep,
            'X-KDE-PluginInfo-Depends=',
            str(self.ledXKDEPluginInfoDepends.text()),
            linesep,
            'X-KDE-PluginInfo-License=',
            str(self.ledXKDEPluginInfoLicense.text()),
            linesep,
            'X-KDE-PluginInfo-EnabledByDefault=',
            str(self.ledXKDEPluginInfoEnabledByDefault.currentText()),
            linesep)))

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

        ACTIONS = '''

        [Desktop Action Name_Your_Command_here]
        Name=Name_Your_Command_here
        Exec=Your_Command_here
        OnlyShowIn=Unity;

        ''' * len(str(self.ledActions.text()).lower().strip().split(';'))

        flnm = str(QFileDialog.getSaveFileName(self.scrollable,
                   " Save Desktop File as ... ", path.expanduser("~"),
                   "Desktop (*.desktop)"))
        f = open(flnm, 'w')

        if self.chooser.currentIndex() is 0 and flnm is not '':
            f.write(''.join(a for a in iter((BASE, UNITY, ACTIONS))))
        elif self.chooser.currentIndex() is 1 and flnm is not '':
            f.write(''.join(a for a in iter((BASE, PLASMA))))
        elif flnm is not '':
            f.write(BASE)
        f.close()

        if self.checkbox2.isChecked() and flnm is not '':
            try:
                chmod(flnm, 0775)  # Py2
            except:
                chmod(flnm, 0o775)  # Py3

        if self.checkbox1.isChecked() and flnm is not '':
            self.process.start('ninja-ide {}'.format(flnm))
            if not self.process.waitForStarted():
                print((" ERROR: Process {} Failed!".format(str(flnm))))
                return

    def processFinished(self):
        ' print info of finished processes '
        print(" INFO: OK: QProcess finished . . . ")


###############################################################################


if __name__ == "__main__":
    print(__doc__)
