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

        QPushButton#status_btn {
            background-color: #4e4e4e;
            color: #fafafa;
            font-size: 18px;
            font-family: Consolas;
        }

        QLabel {
            color: #ffffff;
            background-color: #4e4e4e;
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
