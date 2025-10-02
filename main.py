import keyboard
import pystray
import pyperclip
from PIL import Image, ImageDraw
from time import sleep
from translators.factory import load_translator
import argparse

# Define a variable to control if the keylogger is active
is_active = True

# global translator
translator = load_translator()
translator_language = "Chinese"

# Global variable to control quiet mode
quiet_mode = False

def conditional_print(*args, **kwargs):
    """Print function that respects quiet mode setting"""
    if not quiet_mode:
        print(*args, **kwargs)

def set_translator_language(lang):
    """Set the target translation language"""
    global translator_language
    translator_language = lang
    conditional_print(f"Translation language set to: {lang}")

def is_current_language(lang):
    """Check if the current language is the same as the target language"""
    return lang == translator_language

# --- Hotkey Listener Function ---
def on_key_press(event):
    """Callback function for key press events."""
    global translator
    if is_active and event.name == 'q' and keyboard.is_pressed('ctrl'):
        translate_selected_text()

def translate_selected_text():
    """Handle the text selection, translation, and clipboard update process."""
    global translator, translator_language

    # clear clipboard
    pyperclip.copy("")

    # Simulate Ctrl+C to copy selected text
    keyboard.press_and_release('ctrl+c')
    
    # Small delay to allow clipboard to update
    sleep(0.1)
    
    # Get the selected text from clipboard
    selected_text = ""
    try:
        selected_text = pyperclip.paste()
    except Exception as e:
        print(f"Error getting clipboard content: {e}")
        return
        
    if selected_text and selected_text.strip():
        try:
            # Translate the text to the selected language
            translated_text = translator.translate(translator_language, selected_text)
            
            # debug info
            conditional_print(f"Original text: {selected_text}\n\n")
            conditional_print(f"Translated text: {translated_text}")
            
            # Put the translated text in clipboard
            pyperclip.copy(translated_text)
        except Exception as e:
            conditional_print(f"Translation error: {e}")
    else:
        conditional_print("No text selected or copied")

# --- Tray Icon Functions ---
def create_image():
    """Create a simple icon image for the tray."""
    # Create a blank image with a transparent background
    width = 64
    height = 64
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a simple shape, e.g., a green circle
    draw.ellipse((width*0.1, height*0.1, width*0.9, height*0.9), fill='green', outline='white', width=2)
    return image

def toggle_active(icon, item):
    """Toggle the active state and update the icon color."""
    global is_active
    is_active = not is_active
    
    # Update the icon color based on the state
    icon_image = create_image()
    draw = ImageDraw.Draw(icon_image)
    if is_active:
        draw.ellipse((6, 6, 58, 58), fill='green', outline='white', width=2)
    else:
        draw.ellipse((6, 6, 58, 58), fill='red', outline='white', width=2)
        
    icon.icon = icon_image
    
    conditional_print(f"Key logger is now {'enabled' if is_active else 'disabled'}.")

def exit_app(icon, item):
    """Stop the hotkey listener and exit the application."""
    conditional_print("Exiting application...")
    keyboard.unhook_all()
    icon.stop()

# --- Main Application Logic ---
def main():
    """Main function to set up the tray icon and start the listener."""
    
    global is_active, quiet_mode
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Hotkey translation application')
    parser.add_argument('-q', '--quiet', action='store_true', help='Enable quiet mode to suppress console output')
    args = parser.parse_args()
    
    # Set quiet mode based on argument
    quiet_mode = args.quiet
    
    # Print startup message if not in quiet mode
    conditional_print("Application started. Press Ctrl+Q to translate selected text.")
    if quiet_mode:
        conditional_print("Quiet mode enabled.")
        
    # Create the tray icon image
    image = create_image()
    
    # Create the menu for the tray icon
    menu = (
        pystray.MenuItem('Languages', pystray.Menu(
            pystray.MenuItem('Chinese', lambda item: set_translator_language("Chinese"), checked=lambda item: is_current_language("Chinese"), default=True),
            pystray.MenuItem('English', lambda item: set_translator_language("English"), checked=lambda item: is_current_language("English")),
            pystray.MenuItem('Russian', lambda item: set_translator_language("Russian"), checked=lambda item: is_current_language("Russian")),
            pystray.MenuItem('Japanese', lambda item: set_translator_language("Japanese"), checked=lambda item: is_current_language("Japanese")),
            pystray.MenuItem('Korean', lambda item: set_translator_language("Korean"), checked=lambda item: is_current_language("Korean")),
            pystray.MenuItem('French', lambda item: set_translator_language("French"), checked=lambda item: is_current_language("French")),
        )),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem('Toggle Active', toggle_active),
        pystray.MenuItem('Exit', exit_app),
    )
    
    # Create and run the tray icon
    icon = pystray.Icon('hotkey_app', image, 'Hotkey App', menu)
    
    # Hook the hotkey listener
    keyboard.on_press(on_key_press)
    
    # Run the icon in the main thread
    icon.run()

if __name__ == "__main__":
    main()