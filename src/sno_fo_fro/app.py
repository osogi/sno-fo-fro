import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFileDialog,
    QMessageBox,
    QSizePolicy,
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from sno_fo_fro.analyzer import ImageAnalyzer
from sno_fo_fro.classifier import MockImageClassifier, WeatherClass


classifier = MockImageClassifier()


def get_image_class(path: str) -> WeatherClass:
    metrics = ImageAnalyzer.process_image_by_path(path)
    return classifier.classify(metrics)


class ImageViewerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.image_pixmap = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 800, 600)

        # Create UI elements
        self.image_label = QLabel(self)
        self.image_label.setText("No image selected")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Text label for caption
        self.caption_label = QLabel(self)
        self.caption_label.setAlignment(Qt.AlignCenter)
        self.caption_label.hide()
        self.caption_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        self.open_button = QPushButton("Open Image", self)
        self.open_button.clicked.connect(self.open_image)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)

        # Add caption in a centered horizontal layout
        caption_layout = QHBoxLayout()
        caption_layout.addStretch()
        caption_layout.addWidget(self.caption_label)
        caption_layout.addStretch()
        layout.addLayout(caption_layout)

        layout.addWidget(self.open_button)

        self.setLayout(layout)

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Image File",
            "",
            "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif);;All Files (*)",
            options=options,
        )
        if file_path:
            pixmap = QPixmap(file_path)
            if pixmap.isNull():
                QMessageBox.critical(self, "Error", "Failed to load the image.")
                return

            self.image_pixmap = pixmap
            self.resize_image()

            # Show caption with file path
            weather_res = get_image_class(file_path)
            self.caption_label.setText(f"Weather: {weather_res}")
            self.caption_label.show()

    def resize_image(self):
        """Resize image while keeping the aspect ratio."""
        if self.image_pixmap:
            scaled_pixmap = self.image_pixmap.scaled(
                self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, a0):
        """Handle window resize event to adjust the image size."""
        self.resize_image()
        a0.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = ImageViewerApp()
    viewer.show()
    sys.exit(app.exec())
