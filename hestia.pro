SOURCES = \
    main.py \
    mainwindow.py \
    converter.py \
    filenameeditdialog.py \
    highlighter.py \
    archive/container.py \
    archive/exceptions.py \
    archive/file.py \
    extensions/ruby.py \
    extensions/scenario_paragraph.py \
    extensions/text_span.py \
    extensions/word_link.py \
    models/project.py \
    models/structure.py \
    widgets/plaintextedit.py

FORMS = \
    ui/mainwindow.ui \
    ui/filenameeditdialog.ui

TRANSLATIONS = hestia_ja.ts

RESOURCES = resources.qrc

OTHER_FILES = \
    tools/rcc4.sh \
    tools/rcc5.sh \
    tools/release.sh \
    tools/tr4.sh \
    tools/tr5.sh \
    tools/uic4.sh \
    tools/uic5.sh

# PyQt
CODECFORTR = UTF-8
CODECFORSRC = UTF-8
