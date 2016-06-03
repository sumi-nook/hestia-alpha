SOURCES = \
    main.py \
    mainwindow.py \
    converter.py \
    errormessagedialog.py \
    filenameeditdialog.py \
    glwindow.py \
    highlighter.py \
    qt.py \
    archive/container.py \
    archive/exceptions.py \
    archive/file.py \
    emulator/scene.py \
    extensions/ruby.py \
    extensions/scenario_direction.py \
    extensions/scenario_paragraph.py \
    extensions/text_span.py \
    extensions/word_link.py \
    gl/base.py \
    gl/context.py \
    gl/environment.py \
    gl/figure.py \
    glfont.py \
    gl/image.py \
    gl/text.py \
    gl/texture.py \
    gl/wrapper.py \
    models/project.py \
    models/structure.py \
    utility/bits.py \
    widgets/glwidget.py \
    widgets/plaintextedit.py

FORMS = \
    ui/mainwindow.ui \
    ui/errormessagedialog.ui \
    ui/filenameeditdialog.ui \
    ui/glwindow.ui

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
