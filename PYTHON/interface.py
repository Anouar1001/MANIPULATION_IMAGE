
from PyQt5.QtWidgets import (QInputDialog, QDialog, QTextEdit, QFileDialog)
from PyQt5.QtCore import  QPropertyAnimation

from noir_blanch import *
from image_niveaux_gris import *
from oeimgenmodegris import *
from RGB_GENERATOR import *

import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QStackedWidget,
                             QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
import os
import matplotlib
from PyQt5.QtGui import QIcon
matplotlib.use('Qt5Agg')  # Must be before importing pyplot
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and for PyInstaller """
    if getattr(sys, 'frozen', False):  # Check if running as a bundled executable
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class ImageManipulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Image Manipulation Interface')
        self.setGeometry(100, 100, 1200, 800)  # Made window larger to accommodate plots
        self.setWindowIcon(QIcon(resource_path('icon.jpg')))
        # Initialize img attribute
        self.img = None
        self.current_pixmap = None

        # Store the current plot canvas
        self.current_canvas = None

        # Create main container widget
        self.container = QWidget(self)
        self.container.setGeometry(0, 0, self.width(), self.height())

        # Create layout for the container
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Create background label for video
        self.background_label = QLabel(self)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

        # Initialize video
        video_path = resource_path("background.mp4")
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            print(f"Error: Could not open video file at {video_path}")
            return

        # Create timer for video update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

        # Create stacked widget for UI elements
        self.stacked_widget = QStackedWidget()
        self.layout.addWidget(self.stacked_widget)

        # Create all pages
        self.main_menu = QWidget()
        self.io_page = QWidget()
        self.black_white_page = QWidget()
        self.grayscale_page = QWidget()
        self.resize_page = QWidget()
        self.rgb_page = QWidget()

        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.io_page)
        self.stacked_widget.addWidget(self.black_white_page)
        self.stacked_widget.addWidget(self.grayscale_page)
        self.stacked_widget.addWidget(self.resize_page)
        self.stacked_widget.addWidget(self.rgb_page)


        # Setup all pages
        self.setup_main_menu()
        self.setup_io_page()
        self.setup_black_white_page()
        self.setup_grayscale_page()
        self.setup_resize_page()
        self.setup_rgb_page()

        # Show main menu initially
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def create_embedded_plot(self):
        """Creates and returns a matplotlib figure and canvas embedded in a widget"""
        # Create the figure with a transparent background
        fig = Figure(figsize=(8, 6))
        fig.patch.set_alpha(0.0)
        canvas = FigureCanvas(fig)

        # Create the axes
        ax = fig.add_subplot(111)
        ax.patch.set_alpha(0.7)  # Semi-transparent background for the plot area

        return fig, ax, canvas

    def display_plot_in_widget(self, widget, fig, canvas):
        """Displays a matplotlib plot in the given widget"""
        # Clear any existing layout
        if widget.layout() is not None:
            QWidget().setLayout(widget.layout())

        # Create new layout
        layout = QVBoxLayout(widget)

        # Create a back button
        back_button = QPushButton("Back to Main Menu")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))
        back_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 2px solid #555;
                border-radius: 10px;
                padding: 10px;
                font-size: 14px;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: rgba(200, 200, 200, 200);
            }
        """)

        # Add widgets to layout
        layout.addWidget(back_button)
        layout.addWidget(canvas)

        # Store the current canvas
        self.current_canvas = canvas

    def plot_in_widget(self, widget, plot_function, *args, **kwargs):
        """Creates a plot using the given function and displays it in the widget"""
        # Create new figure and canvas
        fig, ax, canvas = self.create_embedded_plot()

        # Call the plotting function
        plot_function(ax, *args, **kwargs)

        # Display the plot
        self.display_plot_in_widget(widget, fig, canvas)

        # Switch to the widget's page
        self.stacked_widget.setCurrentWidget(widget)
    def setup_main_menu(self):
        # Create a layout for the main menu
        main_menu_layout = QVBoxLayout(self.main_menu)
        main_menu_layout.setContentsMargins(50, 50, 50, 50)
        main_menu_layout.setSpacing(20)  # Add space between buttons

        # Create and style buttons
        button_style = """
        QPushButton {
            background-color: rgba(255, 255, 255, 200); /* Light background */
            border: 2px solid #555; /* Border with gray color */
            border-radius: 10px; /* Rounded corners */
            padding: 10px; /* Padding inside the button */
            font-size: 16px; /* Text size */
            min-width: 200px; /* Minimum button width */
            color: #333; /* Text color */
            transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transitions */
        }
        
        QPushButton:hover {
            background-color: rgba(100, 150, 255, 200); /* Light blue background on hover */
            color: white; /* Text color changes to white on hover */
            border-color: #007BFF; /* Border changes to a matching blue */
        }
        
        QPushButton:pressed {
            background-color: rgba(80, 120, 200, 200); /* Darker blue when pressed */
            border-color: #0056b3; /* Border changes to darker blue */
            color: #eee; /* Slightly dim text color on press */
        }
"""

        # Create buttons for each page
        io_button = QPushButton("Input/Output Operations")
        bw_button = QPushButton("Black & White Operations")
        gray_button = QPushButton("Grayscale Operations")
        resize_button = QPushButton("Resize Operations")
        rgb_button = QPushButton("RGB Operations")

        # Set style for all buttons
        for button in [io_button, bw_button, gray_button, resize_button, rgb_button]:
            button.setStyleSheet(button_style)
            button.setFixedHeight(50)

        # Connect buttons to their respective pages
        io_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.io_page))
        bw_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.black_white_page))
        gray_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.grayscale_page))
        resize_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.resize_page))
        rgb_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.rgb_page))

        # Add buttons to layout
        main_menu_layout.addStretch(1)  # Add space at top
        main_menu_layout.addWidget(io_button, alignment=Qt.AlignCenter)
        main_menu_layout.addWidget(bw_button, alignment=Qt.AlignCenter)
        main_menu_layout.addWidget(gray_button, alignment=Qt.AlignCenter)
        main_menu_layout.addWidget(resize_button, alignment=Qt.AlignCenter)
        main_menu_layout.addWidget(rgb_button, alignment=Qt.AlignCenter)
        main_menu_layout.addStretch(1)  # Add space at bottom

    def update_frame(self):
        ret, frame = self.cap.read()

        if ret:
            if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            scaled_frame = cv2.resize(rgb_frame, (self.width(), self.height()))

            h, w, ch = scaled_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(scaled_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)

            self.background_label.setPixmap(pixmap)
            self.background_label.setGeometry(0, 0, self.width(), self.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.container.setGeometry(0, 0, self.width(), self.height())
        self.background_label.setGeometry(0, 0, self.width(), self.height())

    def closeEvent(self, event):
        self.timer.stop()
        self.cap.release()
        super().closeEvent(event)
    def style_buttons(self, buttons):
        """Apply custom styles to buttons."""
        button_style = """
        QPushButton {
            background-color: rgba(255, 255, 255, 200); /* Light background */
            border: 2px solid #555; /* Border with gray color */
            border-radius: 10px; /* Rounded corners */
            padding: 10px; /* Padding inside the button */
            font-size: 16px; /* Text size */
            min-width: 200px; /* Minimum button width */
            color: #333; /* Text color */
            transition: background-color 0.3s ease, color 0.3s ease; /* Smooth transitions */
        }
        
        QPushButton:hover {
            background-color: rgba(100, 150, 255, 200); /* Light blue background on hover */
            color: white; /* Text color changes to white on hover */
            border-color: #007BFF; /* Border changes to a matching blue */
        }
        
        QPushButton:pressed {
            background-color: rgba(80, 120, 200, 200); /* Darker blue when pressed */
            border-color: #0056b3; /* Border changes to darker blue */
            color: #eee; /* Slightly dim text color on press */
        }
        """

        for button in buttons:
            button.setStyleSheet(button_style)

    def get_dimensions(self):
        """Get height and width from user via dialog boxes"""
        height, ok = QInputDialog.getInt(
            self, 'Input', 'Enter height (pixels):',
            value=512, min=1, max=2000
        )
        if not ok:
            return None, None

        width, ok = QInputDialog.getInt(
            self, 'Input', 'Enter width (pixels):',
            value=512, min=1, max=2000
        )
        if not ok:
            return None, None

        return height, width

    def convert_np_to_qpixmap(self, np_img):
        """Convert numpy array to QPixmap for display"""
        height, width = np_img.shape
        bytes_per_line = width
        q_img = QImage(np_img.data, width, height, bytes_per_line, QImage.Format_Grayscale8)
        return QPixmap.fromImage(q_img)


    def setup_io_page(self):
        """Set up the I/O page."""
        layout = QVBoxLayout()

        # Create QLabel to display the image
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.image_label)

        back_button = QPushButton("Retour", self)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))

        self.load_button = QPushButton('Charger une Image', self)
        self.load_button.clicked.connect(self.load_image)

        self.save_button = QPushButton('Enregistrer une Image', self)
        self.save_button.clicked.connect(self.save_image)

        self.show_button = QPushButton('Afficher une Image', self)
        self.show_button.clicked.connect(self.AfficherImg)

        # Style buttons
        self.style_buttons([self.load_button, self.save_button, self.show_button, back_button])

        layout.addWidget(self.load_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.show_button)
        layout.addWidget(back_button)
        self.io_page.setLayout(layout)
    def setup_black_white_page(self):
        """Set up the black and white page with four buttons."""
        layout = QVBoxLayout()

        # Back button to return to the main menu
        back_button = QPushButton("Retour", self)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))

        # Button to generate a white image
        image_blanche_button = QPushButton("Image Blanche", self)
        image_blanche_button.clicked.connect(self.create_white_image)

        # Button to generate a black image
        image_noir_button = QPushButton("Image Noir", self)
        image_noir_button.clicked.connect(self.create_black_image)

        # Button to convert image to black and white pattern
        image_blancl_n = QPushButton("Image Blanc et Noir", self)
        image_blancl_n.clicked.connect(self.convert_to_black_and_white)

        # Button to create a negative of the image
        image_negative_button = QPushButton("Image Négative", self)
        image_negative_button.clicked.connect(self.create_negative_image)

        # Style buttons
        self.style_buttons(
            [image_blanche_button, image_noir_button, image_blancl_n, image_negative_button, back_button]
        )
        # Add all the buttons to the layout
        layout.addWidget(image_blanche_button)
        layout.addWidget(image_noir_button)
        layout.addWidget(image_blancl_n)
        layout.addWidget(image_negative_button)
        layout.addWidget(back_button)

        # Set layout to the page
        layout.setAlignment(Qt.AlignCenter)
        self.black_white_page.setLayout(layout)

    def create_white_image(self):
        """Handler for white image button"""
        h, w = self.get_dimensions()
        if h is None or w is None:
            return

        try:
            # Call your existing function
            white_img = image_blanche(h, w)

            # Convert to PIL Image and then to QPixmap for display
            self.img = Image.fromarray(white_img)
            self.current_pixmap = self.convert_np_to_qpixmap(white_img)
            self.AfficherImg()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to create white image: {str(e)}')

    def create_black_image(self):
        """Handler for black image button"""
        h, w = self.get_dimensions()
        if h is None or w is None:
            return

        try:
            # Call your existing function
            black_img = image_noire(h, w)

            # Convert for display
            self.img = Image.fromarray(black_img)
            self.current_pixmap = self.convert_np_to_qpixmap(black_img)
            self.AfficherImg()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to create black image: {str(e)}')

    def convert_to_black_and_white(self):
        """Handler for black and white pattern button"""
        h, w = self.get_dimensions()
        if h is None or w is None:
            return

        try:
            # Call your existing function
            bw_img = creer_img_blanc_noir(h, w)

            # Convert for display
            self.img = Image.fromarray(bw_img)
            self.current_pixmap = self.convert_np_to_qpixmap(bw_img)
            self.AfficherImg()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to create black and white pattern: {str(e)}')

    def create_negative_image(self):
        """Handler for negative image button"""
        try:
            # Open file dialog for user to choose an image
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                "Choose an image",
                "",
                "Image Files (*.png *.jpg *.bmp *.jpeg *.gif)"
            )

            if not file_path:  # If user cancels the dialog
                return

            # Load the selected image and convert to grayscale
            self.img = Image.open(file_path).convert('L')  # 'L' mode = grayscale

            # Convert PIL image to numpy array
            img_array = np.array(self.img)

            # Create negative image
            neg_img = negatif(img_array)

            # Afficher l'image originale et son négatif côte à côte
            plt.figure(figsize=(12, 6))

            # Image originale
            plt.subplot(1, 2, 1)
            plt.imshow(img_array, cmap='gray')
            plt.title('Image Originale')
            plt.axis('off')

            # Image négative
            plt.subplot(1, 2, 2)
            plt.imshow(neg_img, cmap='gray')
            plt.title('Image Négative')
            plt.axis('off')

            plt.show()

        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to process image: {str(e)}')
    def setup_grayscale_page(self):
        """Set up the grayscale page."""
        layout = QVBoxLayout()

        back_button = QPushButton("Retour", self)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))

        lumninence = QPushButton('luminance', self)
        lumninence.clicked.connect(self.lumin)

        cntrast = QPushButton('contrast', self)
        cntrast.clicked.connect(self.contra)

        profndeur = QPushButton('profondeur', self)
        profndeur.clicked.connect(self.profn)

        Ovrir = QPushButton('Ouvrir', self)
        Ovrir.clicked.connect(self.ou_vrir)

        # Style buttons
        self.style_buttons([lumninence, cntrast, profndeur, Ovrir, back_button])

        layout.addWidget(Ovrir)
        layout.addWidget(profndeur)
        layout.addWidget(cntrast)
        layout.addWidget(lumninence)
        layout.addWidget(back_button)
        layout.setAlignment(Qt.AlignCenter)
        self.grayscale_page.setLayout(layout)
    def ou_vrir(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "","Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        i = Ouvrir(file_path)
        self.afficher_matrice(i)
    def afficher_matrice(self, matrice):
        # Créer un message box avec un QTextEdit pour afficher la matrice
        dialog = QDialog(self)
        dialog.setWindowTitle("Matrice de l'image")

        # Convertir la matrice en chaîne de texte lisible
        matrice_text = '\n'.join([' '.join(map(str, row)) for row in matrice])

        # Ajouter un QTextEdit pour afficher la matrice avec défilement
        layout = QVBoxLayout()

        text_edit = QTextEdit(dialog)
        text_edit.setReadOnly(True)
        text_edit.setText(matrice_text)  # Afficher la matrice complète

        # Bouton pour fermer la fenêtre
        close_button = QPushButton("Fermer", dialog)
        close_button.clicked.connect(dialog.accept)

        layout.addWidget(text_edit)
        layout.addWidget(close_button)

        dialog.setLayout(layout)
        dialog.exec_()
    def profn(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "","Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        i = profondeur(file_path)
        QMessageBox.information(self, "Profendeur", f"profendeur: {i}")
    def contra(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "","Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        i = contrast(file_path)
        QMessageBox.information(self, "Contrast", f"contrast: {i}")
    def lumin(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")
        i = luminance(file_path)
        QMessageBox.information(self, "Luminance", f"Luminance: {i}")
    def setup_resize_page(self):
        """Set up the resize page."""
        layout = QVBoxLayout()

        back_button = QPushButton("Retour", self)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))

        inverse_button = QPushButton("inverser une image", self)
        inverse_button.clicked.connect(self.invimg)
        fliph_button = QPushButton("symetrie d'axe vertical", self)
        fliph_button.clicked.connect(self.flihimg)
        poserv_button = QPushButton("posant img1 sur img2 verticalement", self)
        poserv_button.clicked.connect(self.posvimg)
        poserh_button = QPushButton("posant img1 sur img2 horizentalement", self)
        poserh_button.clicked.connect(self.poshimg)
        self.style_buttons([inverse_button, fliph_button, poserv_button, poserh_button, back_button])

        layout.addWidget(inverse_button)
        layout.addWidget(fliph_button)
        layout.addWidget(poserv_button)
        layout.addWidget(poserh_button)
        layout.addWidget(back_button)
        layout.setAlignment(Qt.AlignCenter)
        self.resize_page.setLayout(layout)
    def invimg(self):
        try:
            chemin = self.obtenirCheminFichier()
            if not chemin:
                raise ValueError("Aucun fichier sélectionné.")
            MAT = self.image_to_matrix(chemin)
            INV = inverser_i(MAT)
            self.AfficherImg_1(INV, "image inverse")
        except Exception as e:
            afficher_erreur(str(e))
    def flihimg(self):
        try:
            chemin = self.obtenirCheminFichier()
            if not chemin:
                raise ValueError("Aucun fichier sélectionné.")
            MAT = self.image_to_matrix(chemin)
            flipped = flipH(MAT)
            self.AfficherImg_1(flipped, "Image Retournée Horizontalement")
        except Exception as e:
            afficher_erreur(str(e))
    def poshimg(self):
        '''
        def test_poserH():
            try:
                chemin = obtenirCheminFichier()
                if not chemin:
                    raise ValueError("Aucun fichier sélectionné.")
                MAT = image_to_matrix(chemin)
                H = poserH(MAT, MAT)
                AfficherImg(H, "Superposition Horizontale")
            except Exception as e:
                afficher_erreur(str(e))
        '''
        """
            Fonction de test pour superposer horizontalement deux images sélectionnées par l'utilisateur.
            """
        try:
            # Demander à l'utilisateur de sélectionner la première image
            chemin1 = self.obtenirCheminFichier()
            if not chemin1:
                print("Aucune première image sélectionnée.")
                return

            # Charger la première image en matrice
            img1 = self.image_to_matrix(chemin1)

            # Demander à l'utilisateur de sélectionner la deuxième image
            chemin2 = self.obtenirCheminFichier()
            if not chemin2:
                print("Aucune deuxième image sélectionnée.")
                return

            # Charger la deuxième image en matrice
            img2 = self.image_to_matrix(chemin2)

            # Appliquer la fonction poserH pour superposer les deux images
            resultat = poserH(img1, img2)

            # Afficher le résultat
            print("Superposition horizontale réussie !")
            self.AfficherImg_1(resultat)
        except Exception as e:
            print(f"Erreur : {e}")
    def posvimg(self):
        '''
        def test_poserV():
            try:
                chemin = obtenirCheminFichier()
                if not chemin:
                    raise ValueError("Aucun fichier sélectionné.")
                MAT = image_to_matrix(chemin)
                V = poserV(MAT, MAT)
                AfficherImg(V, "Superposition Verticale")
            except Exception as e:
                afficher_erreur(str(e))
        '''
        """
            Fonction de test pour superposer verticalement deux images sélectionnées par l'utilisateur.
            """
        try:
            # Demander à l'utilisateur de sélectionner la première image
            chemin1 = self.obtenirCheminFichier()
            if not chemin1:
                print("Aucune première image sélectionnée.")
                return

            # Charger la première image en matrice
            img1 = self.image_to_matrix(chemin1)

            # Demander à l'utilisateur de sélectionner la deuxième image
            chemin2 = self.obtenirCheminFichier()
            if not chemin2:
                print("Aucune deuxième image sélectionnée.")
                return

            # Charger la deuxième image en matrice
            img2 = self.image_to_matrix(chemin2)

            # Appliquer la fonction poserV pour superposer les deux images
            resultat = poserV(img1, img2)

            # Afficher le résultat
            print("Superposition verticale réussie !")
            self.AfficherImg_1(resultat)
        except Exception as e:
            print(f"Erreur : {e}")
    def obtenirCheminFichier(self):
        """
        boite de dialogue ==== selection d image
        """
        file_path, _ = QFileDialog.getOpenFileName(None, "Open Image", "", "Image Files (*.png *.jpg *.bmp *.tiff)")
        return file_path
    def image_to_matrix(self, image_path):
        """
        Convertit une image en une matrice NumPy.
        """
        try:
            img = plt.imread(image_path)
            return img
        except Exception as e:
            raise ValueError(f"Impossible de lire l'image : {e}")
    def AfficherImg_1(self, img, titre="Image"):
        """
        Affiche une image à l'écran.
        """
        plt.axis("off")
        plt.title(titre)  # Use the provided title
        plt.imshow(img, cmap="gray", interpolation="nearest")
        plt.show()
    def setup_rgb_page(self):
        """Set up the RGB page."""
        layout = QVBoxLayout()

        back_button = QPushButton("Retour", self)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.main_menu))

        rotate_button = QPushButton("initImageRGB", self)
        rotate_button.clicked.connect(self.initimgrgb)
        symetrie_h_1 = QPushButton("symetrie horizental", self)
        symetrie_h_1.clicked.connect(self.symetrihrgb)
        symetrie_v_1 = QPushButton("symetrie vertical", self)
        symetrie_v_1.clicked.connect(self.symetrivrgb)
        grayscale_1 = QPushButton("grayscale RGB", self)
        grayscale_1.clicked.connect(self.grayscalrgb)
        # Style buttons
        self.style_buttons([rotate_button, symetrie_v_1, symetrie_h_1, grayscale_1, back_button])

        layout.addWidget(rotate_button)
        layout.addWidget(symetrie_h_1)
        layout.addWidget(symetrie_v_1)
        layout.addWidget(grayscale_1)
        layout.addWidget(back_button)
        layout.setAlignment(Qt.AlignCenter)
        self.rgb_page.setLayout(layout)
    def initimgrgb(self):
        h,v = self.get_dimensions()
        if h is None or v is None:
            return
        try:
            image_rgb = np.zeros((h,v,3))
            image_e = initImageRGB(image_rgb)
            plt.axis("off")
            plt.imshow(image_e)
            plt.show()
            self.afficher_matrice(image_e)
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Failed to create white image: {str(e)}')
    def symetrihrgb(self):
        image_path = self.obtenirCheminFichier()
        image_rgb_h = symetrie_h(image_path)
        plt.axis("off")
        plt.imshow(image_rgb_h)
        plt.show()
    def symetrivrgb(self):
        image_path = self.obtenirCheminFichier()
        image_rgb_v = symetrie_V(image_path)
        plt.axis("off")
        plt.imshow(image_rgb_v)
        plt.show()
    def grayscalrgb(self):
        image_rgb_path = self.obtenirCheminFichier()
        image_rgb_grayscale = grayscale(image_rgb_path)
        plt.axis("off")
        plt.imshow(image_rgb_grayscale, cmap = "gray")
        plt.show()

    def load_image(self):
        """Function to load an image."""
        file_path, _ = QFileDialog.getOpenFileName(self,"Open Image","","Image Files (*.png *.jpg *.bmp *.jpeg *.gif)")

        if file_path:
            try:
                # Load the image using PIL
                image = Image.open(file_path)
                self.img = image

                # Convert PIL image to QPixmap
                self.current_pixmap = QPixmap(file_path)

                # Display the image
                self.AfficherImg()
                print(f"Loaded image from: {file_path}")

            except Exception as e:
                print(f"Error loading image: {e}")
        else:
            print("No file selected.")
    def AfficherImg(self):
        """Function to display an image."""
        if self.current_pixmap is not None:
            # Calculate scaling to fit the window while maintaining aspect ratio
            label_size = self.image_label.size()
            scaled_pixmap = self.current_pixmap.scaled(
                label_size,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )

            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            print("Displaying the image...")
        else:
            print("No image loaded.")
    def save_image(self):
        """Function to save an image."""
        if self.img is not None:
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save Image",
                "",
                "Image Files (*.png *.jpg *.bmp *.jpeg)"
            )

            if file_path:
                try:
                    # Save the image using PIL
                    self.img.save(file_path)
                    print(f"Image saved to: {file_path}")
                except Exception as e:
                    print(f"Error saving image: {e}")
            else:
                print("No file selected for saving.")
        else:
            print("No image loaded to save.")
    def style_buttons(self, buttons):
        """Apply custom styles to buttons."""
        button_style = """
        QPushButton {
            font-size: 16px;
            background-color: #3C3C3C;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        QPushButton:hover {
            background-color: #505050;
        }
        QPushButton:pressed {
            background-color: #282828;
        }
        """
        for button in buttons:
            button.setStyleSheet(button_style)

    def add_click_effect(self, button):
        """Add a click effect to buttons."""
        def on_pressed():
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(150)
            animation.setStartValue(button.geometry())
            animation.setEndValue(button.geometry().adjusted(-5, -5, 5, 5))
            animation.start()

        def on_released():
            animation = QPropertyAnimation(button, b"geometry")
            animation.setDuration(150)
            animation.setStartValue(button.geometry().adjusted(-5, -5, 5, 5))
            animation.setEndValue(button.geometry())
            animation.start()

        button.pressed.connect(on_pressed)
        button.released.connect(on_released)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageManipulator()
    window.show()
    sys.exit(app.exec_())