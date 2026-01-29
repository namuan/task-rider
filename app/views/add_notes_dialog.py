from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox


class AddNotesDialog(QDialog):
    def __init__(self, parent=None, current_notes=""):
        super().__init__(parent)
        self.setWindowTitle("Add Notes")
        self.resize(400, 300)

        self.layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setPlainText(current_notes)
        self.layout.addWidget(self.text_edit)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel,
            self,
        )
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_notes(self):
        return self.text_edit.toPlainText()
