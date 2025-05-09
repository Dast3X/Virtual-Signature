from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTabWidget, QTextEdit, QScrollArea, QWidget, QPushButton,
                               QHBoxLayout)

from src.utils.utils import get_assets_path


class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super(HelpDialog, self).__init__(parent)
        self.setWindowTitle("User Guide")
        self.setWindowIcon(QIcon(get_assets_path("logo.png")))
        self.resize(800, 600)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Create tabs for different help sections
        tab_widget = QTabWidget()

        # Add tabs with content
        tab_widget.addTab(self.create_overview_tab(), "Overview")
        tab_widget.addTab(self.create_camera_settings_tab(), "Camera Settings")
        tab_widget.addTab(self.create_signature_settings_tab(), "Signature Settings")
        tab_widget.addTab(self.create_usage_guide_tab(), "Usage Guide")
        tab_widget.addTab(self.create_gesture_guide_tab(), "Gesture Guide")
        tab_widget.addTab(self.create_troubleshooting_tab(), "Troubleshooting")

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(close_button)

        main_layout.addWidget(tab_widget)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def create_scrollable_text(self, content):
        """Creates a scrollable area with text"""
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        text_container = QWidget()
        layout = QVBoxLayout(text_container)

        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setHtml(content)

        layout.addWidget(text_edit)
        scroll_area.setWidget(text_container)

        return scroll_area

    def create_overview_tab(self):
        """Creates a tab with a general overview of the application"""
        content = """
        <h2 style="color:#2c3e50;">🔍 Application Overview</h2>
        <p style="font-size: 16px; color:#34495e;">This application is designed for recognizing and working with signatures through a webcam. 
        It allows you to capture, analyze, and save signatures in digital format.</p>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">🚀 Main Features:</h3>
            <ul style="color:#34495e;">
                <li>Webcam image capture for signature tracking.</li>
                <li>Gesture recognition for creating digital signatures.</li>
                <li>Adjustable camera and recognition sensitivity settings.</li>
                <li>Signature display parameter adjustments.</li>
                <li>Saving signatures in various formats, including image files.</li>
            </ul>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">🖥️ Application Interface:</h3>
            <p style="color:#34495e;">The application interface consists of the following main elements:</p>
            <ul style="color:#34495e;">
                <li><b>Main Window:</b> Displays the live camera feed and overlaid signature.</li>
                <li><b>Camera Settings Dock Panel:</b> Allows you to adjust camera parameters for optimal recognition.</li>
                <li><b>Signature Settings Dock Panel:</b> Lets you adjust the appearance and display parameters of the signature.</li>
                <li><b>Status Bar:</b> Displays real-time information about finger position and the current number of signature points.</li>
            </ul>
        </section>
        """
        return self.create_scrollable_text(content)

    def create_camera_settings_tab(self):
        """Creates a tab with information about camera settings"""
        content = """
        <h2 style="color:#2c3e50;">📷 Camera Settings</h2>
        <p style="font-size: 16px; color:#34495e;">This panel allows you to adjust gesture recognition and camera operation parameters:</p>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">⚙️ Main Elements:</h3>
            <ul style="color:#34495e;">
                <li><b>Camera Selection:</b> Choose the image capture device if multiple cameras are connected.</li>
                <li><b>Resolution:</b> Adjust the resolution of the video stream.</li>
                <li><b>FPS:</b> Change the FPS (frames per second) of the video stream.</li>
                <li><b>Start/Stop:</b> Button to start or stop image capture from the camera.</li>
                <li><b>Advanced Settings:</b> Open settings to adjust saturation, brightness, grain, HSV, and more (only available if your camera drivers support these settings, not available for built-in cameras).</li>
            </ul>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">🔧 Setting Recommendations:</h3>
            <ul style="color:#34495e;">
                <li>Ensure good lighting to improve recognition.</li>
                <li>Start by adjusting the HSV sliders and contrast for optimal results.</li>
            </ul>
        </section>
        """
        return self.create_scrollable_text(content)

    def create_signature_settings_tab(self):
        """Creates a tab with information about signature settings"""
        content = """
        <h2 style="color:#2c3e50;">✍️ Signature Settings</h2>
        <p style="font-size: 16px; color:#34495e;">This panel allows you to adjust the display and saving parameters of the signature:</p>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">⚙️ Main Elements:</h3>
            <ul style="color:#34495e;">
                <li><b>Minimum Distance:</b> Set the minimum distance required for drawing.</li>
                <li><b>Maximum Distance:</b> Set the maximum distance allowed for drawing.</li>
                <li><b>Minimum Points:</b> Set the minimum points required to save the signature.</li>
                <li><b>Save Duration:</b> Adjust the time required to save the signature.</li>
                <li><b>Clear:</b> Remove the current signature.</li>
                <li><b>Reset:</b> Reset settings to their default values.</li>
                <li><b>Save:</b> Save the signature to a file.</li>
            </ul>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">✍️ Creating a Signature:</h3>
            <p style="color:#34495e;">To create a signature, move your marker (finger) within the camera's field of view. 
            The system will track your movements and generate a visual representation of the signature.</p>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">💾 Saving the Signature:</h3>
            <p style="color:#34495e;">When you finish creating your signature, click the "Save" button to save it as an image file.</p>
        </section>

        <section>
            <h3 style="color:#2980b9;">💡 Tips for Creating Signatures:</h3>
            <ul style="color:#34495e;">
                <li>Keep your hand steady to get a clearer signature.</li>
                <li>For more complex signatures, move your hand more slowly.</li>
                <li>For the best results, maintain a consistent distance from the camera.</li>
            </ul>
        </section>
        """
        return self.create_scrollable_text(content)

    def create_usage_guide_tab(self):
        """Creates a tab with usage guide"""
        content = """
        <h2 style="color:#2c3e50;">Usage Guide</h2>

        <section style="margin-bottom: 25px;">
            <h3 style="color:#2980b9;">🚀 Getting Started:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li>Launch the application.</li>
                <li>Make sure your webcam is connected and working.</li>
                <li>Click the "Start" button in the camera settings panel to activate the camera.</li>
            </ol>
        </section>

        <section style="margin-bottom: 25px;">
            <h3 style="color:#2980b9;">✍️ Creating a Signature:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li>After setting the recognition parameters and activating the camera, bring the hand into the camera's field of view.</li>
                <li>Point your index finger upward to start drawing (all other fingers should be down).</li>
                <li>Move your finger to draw your signature — the application will track your finger movement.</li>
                <li>You can pause drawing by moving your hand out of the camera's field of view.</li>
                <li>Return to the field of view with the pointing gesture to continue drawing.</li>
            </ol>
        </section>

        <section style="margin-bottom: 25px;">
            <h3 style="color:#2980b9;">✋ Gesture Controls:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li><strong>Point Up:</strong> Point your index finger up (all other fingers down) to start drawing.</li>
                <li><strong>Move Finger:</strong> Move your pointed finger to draw your signature.</li>
                <li><strong>Thumbs Down:</strong> Show a thumbs down gesture to clear the canvas and start over.</li>
                <li><strong>Thumbs Up:</strong> Show a thumbs up gesture and hold it to save the signature to a file.</li>
            </ol>
        </section>

        <section style="margin-bottom: 25px;">
            <h3 style="color:#2980b9;">⚙️ Signature Settings:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li>Adjust the minimum and maximum distance sliders to set the sensitivity of the signature recognition.</li>
                <li>Change the minimum points slider to set the minimum number of points required for saving the signature.</li>
                <li>Adjust the save duration slider to set the time for saving the signature.</li>
                <li>Use the "Clear" button to remove the current signature if needed.</li>
                <li>Click the "Reset" button to restore default settings.</li>
                <li>Click the "Save" button to save the signature.</li>
            </ol>
        </section>

        <section style="margin-bottom: 25px;">
            <h3 style="color:#2980b9;">💾 Saving the Result:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li>When you finish creating the signature, show a thumbs up gesture and hold it for the set duration.</li>
                <li>Alternatively, click the "Save" button in the signature settings panel.</li>
                <li>In the save dialog that appears, choose a location and format to save your signature.</li>
            </ol>
        </section>

        <section>
            <h3 style="color:#2980b9;">📝 Creating a New Signature:</h3>
            <ol style="font-size: 16px; line-height: 1.6;">
                <li>To create a new signature, show a thumbs down gesture.</li>
                <li>Alternatively, click the "Clear" button in the signature settings panel.</li>
                <li>The canvas will be cleared, and you can begin drawing a new signature.</li>
            </ol>
        </section>
        """
        return self.create_scrollable_text(content)

    def create_gesture_guide_tab(self):
        """Creates a tab with detailed gesture controls and animations"""
        content = f"""
        <h2>Gesture Controls Guide</h2>
        <p>This application uses hand gestures to control drawing and saving functions. 
        Below are the main gestures you'll use:</p>

        <table width="100%" border="0" cellpadding="10">
            <tr>
                <td width="120" valign="top">
                    <img src="{get_assets_path("pointing_up.png")}" alt="Point index finger up" width="100">
                </td>
                <td valign="top">
                    <h3>Point Up - Start Drawing</h3>
                    <p>Raise your index finger while keeping all other fingers down to begin drawing. 
                    The system will track the tip of your index finger to create the signature.</p>
                </td>
            </tr>

            <tr>
                <td width="120" valign="top">
                    <img src="{get_assets_path("moving.png")}" alt="Move finger to draw" width="100">
                </td>
                <td valign="top">
                    <h3>Move Finger - Draw Signature</h3>
                    <p>With your index finger pointed up, move your hand to draw your signature. 
                    The application tracks the movement and converts it into a continuous line.</p>
                </td>
            </tr>

            <tr>
                <td width="120" valign="top">
                    <img src="{get_assets_path("thumbs_down.png")}" alt="Thumbs down gesture" width="100">
                </td>
                <td valign="top">
                    <h3>Thumbs Down - Clear Canvas</h3>
                    <p>Show a thumbs down gesture to clear the current signature from the canvas.
                    This allows you to start over if you're not satisfied with your current signature.</p>
                </td>
            </tr>

            <tr>
                <td width="120" height="10" valign="top">
                    <img src="{get_assets_path("thumbs_up.png")}" alt="Thumbs up gesture" width="100">
                </td>
                <td valign="top">
                    <h3>Thumbs Up - Save Signature</h3>
                    <p>Show a thumbs up gesture and hold it in this position to save your signature.
                    Hold the gesture for the duration set in the signature settings panel to trigger the save function.</p>
                </td>
            </tr>
        </table>

        <h3>Tips for Better Gesture Recognition:</h3>
        <ul>
            <li>Ensure your hand is well-lit and clearly visible to the camera</li>
            <li>Keep your gestures clear and distinct - fully extend or close fingers as needed</li>
            <li>Hold your hand at a comfortable distance from the camera - not too close or too far</li>
            <li>Make sure your hand is fully in the camera's field of view</li>
            <li>For drawing, try to keep your hand at a consistent distance from the camera</li>
        </ul>
        """
        return self.create_scrollable_text(content)

    def create_troubleshooting_tab(self):
        """Creates a tab with troubleshooting information"""
        content = """
        <h2 style="color:#2c3e50;">Troubleshooting Guide</h2>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">📷 Camera Not Working</h3>
            <p><strong>Problem:</strong> After clicking "Start," the camera image does not appear.</p>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Make sure the camera is properly connected to the computer.</li>
                <li>Check if the camera is being used by another application.</li>
                <li>Try selecting a different camera from the list of available devices.</li>
                <li>Ensure the application path contains only ASCII (English) characters.</li>
                <li>Restart the application.</li>
            </ul>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">✋ Gesture Recognition Issues</h3>
            <p><strong>Problem:</strong> The application doesn't recognize your hand gestures correctly.</p>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Ensure your hand is well-lit and clearly visible.</li>
                <li>Make your gestures more distinct and hold them steady.</li>
                <li>Try adjusting your distance from the camera.</li>
                <li>Check the camera settings for better visibility.</li>
            </ul>
        </section>

        <section style="margin-bottom: 20px;">
            <h3 style="color:#2980b9;">🖊️ Drawing Issues</h3>
            <p><strong>Problem:</strong> The signature appears jumpy or disconnected.</p>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Move your finger more slowly and steadily.</li>
                <li>Adjust the minimum and maximum distance settings.</li>
                <li>Ensure there's adequate lighting to track your finger.</li>
                <li>Maintain a consistent distance from the camera.</li>
            </ul>
        </section>

        <section>
            <h3 style="color:#2980b9;">💾 Saving Issues</h3>
            <p><strong>Problem:</strong> The signature won't save when using the thumbs up gesture.</p>
            <p><strong>Solutions:</strong></p>
            <ul>
                <li>Hold the thumbs up gesture longer and more steadily.</li>
                <li>Increase the save duration in the signature settings.</li>
                <li>Ensure you have enough points in your signature (check minimum points setting).</li>
                <li>Alternatively, use the "Save" button in the signature settings panel.</li>
            </ul>
        </section>
        """
        return self.create_scrollable_text(content)
