def style_main(self):
    stylesheet = """
        QMainWindow {
            background-color: #2a2a2a;
        }

        QMenuBar {
            background-color: #2e2e2e;
            color: #e0e0e0;
            font: bold;
            font-size: 16px;
            font-family: Consolas;
        }

        QMenuBar::item {
            background-color: transparent;
        }

        QMenuBar::item:selected {
            background-color: #ffffff;
            color: #2e2e2e;
        }

        QMenu {
            background-color: #2e2e2e;
            color: #ffffff;
            font: bold;
            font-size: 16px;
            font-family: Consolas;
        }

        QMenu::item:selected {
            background-color: #ffffff;
            color: #2e2e2e;
        }

        QPushButton {
            background-color: #4e4e4e;
            color: #fafafa;
            font: bold;
            font-size: 18px;
            font-family: Consolas;
        }

        QLabel {
            color: #ffffff;
            font: bold;
            font-size: 18px;
            font-family: Consolas;
        }

        QLabel#video {
            color: #ffffff;
            background-color: #4e4e4e;
            font-size: 50px;
            font-family: Consolas;
        }

        QLabel#status_lb {
            background-color: #2e2e2e;
            color: #ffffff;
            margin-left: 2px;
            margin-right: 2px;
            font-size: 18px;
            font-family: Consolas;
        }

        QStatusBar::item {
            border: 0px;
        }

        QTextEdit {
            background-color: #4e4e4e;
            border: 0px;
            color: #ffffff;
            font: bold;
            font-size: 17px;
            font-family: Consolas;
        }
    """

    return stylesheet


def style_statusbar(self):
    stylesheet = """
        color: #ffffff;
        background-color: #2e2e2e;
        font-size: 18px;
        font-family: Consolas;
    """

    return stylesheet
