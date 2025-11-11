# Que

Que is a lightweight system tray application that enables quick text translation using keyboard shortcuts. Simply select any text and press your configured hotkey (default: `Ctrl+Q`) to translate it to your chosen language, with the translated text automatically copied to your clipboard.

## Features

- System tray application that runs in the background
- Translate selected text with a configurable keyboard shortcut (default: `Ctrl+Q`)
- Customizable hotkey configuration in `config.json`
- Support for multiple translation providers (Gemini, OpenAI, and compatible APIs)
- Configurable target languages with customizable defaults
- Quick language switching through system tray menu
- Toggle activation on/off through the system tray menu
- Translated text automatically copied to clipboard for easy pasting

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/g0g5/Que.git
   cd Que
   ```

2. Install the required dependencies using `uv` (recommended):
   ```
   uv sync
   ```

3. Configure your translation provider by copying `config.example.json` to `config.json`:
   ```
   cp config.example.json config.json
   ```

4. Edit `config.json` to add your API key for your chosen translation provider.

## Configuration

Edit the `config.json` file to set up your preferred translation service and target languages:

```json
{
    "hotkey": "ctrl+q",
    "provider": "Gemini",
    "default_language": "Chinese",
    "languages": [
        {
            "name": "Chinese",
            "code": "zh",
            "default": true
        },
        {
            "name": "English",
            "code": "en"
        },
        {
            "name": "Japanese",
            "code": "ja"
        },
        {
            "name": "Spanish",
            "code": "es"
        }
    ],
    "providers": [
        {
            "provider_name": "Gemini",
            "provider_type": "GeminiAPI",
            "api_key": "YOUR_GEMINI_API_KEY",
            "model": "gemini-2.5-flash"
        },
        {
            "provider_name": "OpenAI",
            "provider_type": "OpenAICompatible",
            "base_url": "https://api.openai.com/v1",
            "api_key": "YOUR_OPENAI_API_KEY",
            "model": "gpt-5-mini"
        }
    ]
}
```

### Hotkey Configuration

- **`hotkey`**: The keyboard shortcut to trigger translation (default: `"ctrl+q"`)
  - Format: `"modifier+key"` or `"modifier1+modifier2+key"`
  - Examples:
    - `"ctrl+q"` - The default hotkey
    - `"alt+t"` - Alt + T
    - `"ctrl+shift+r"` - Ctrl + Shift + R
  - Supported modifiers: `ctrl`, `alt`, `shift`
  - The hotkey is case-insensitive

### Language Configuration

- **`default_language`**: The language selected when the application starts (must match one of the language names)
- **`languages`**: Array of available target languages shown in the system tray menu
  - **`name`**: Display name for the language (required)
  - **`code`**: Language code (optional, for future API integration)
  - **`default`**: Mark this language as the default (optional)

You can add, remove, or reorder languages in the `languages` array to customize the menu. If no language configuration is provided, the application will use a default set of languages (Chinese, English, Russian, Japanese, Korean, French).

### Translation Providers

Supported providers:
- Google Gemini
- OpenAI
- Other OpenAI-compatible APIs (including Moonshot AI, etc.)

## Usage

1. Run the application:
   ```
   uv run python main.py
   ```

2. Look for the green dot icon in your system tray, indicating the app is active.

3. To translate text:
   - Select the text you want to translate
   - Press your configured hotkey (default: `Ctrl+Q`)
   - The translated text will automatically be copied to your clipboard

4. Right-click the tray icon to:
   - Switch between different target languages (configured in `config.json`)
   - Toggle the application on/off
   - Exit the application

When the application is inactive (red dot icon), the configured hotkey will not work.

## Requirements

- Python 3.10 or newer
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Windows OS (due to [keyboard](https://github.com/boppreh/keyboard) library limitations)
- Internet connection for translation services

## Libraries Used

- [keyboard](https://github.com/boppreh/keyboard) - For global hotkey detection
- [pystray](https://github.com/moses-palmer/pystray) - For system tray icon
- [pyperclip](https://github.com/asweigart/pyperclip) - For clipboard operations
- [Pillow](https://python-pillow.org/) - For creating the system tray icon
- Various API client libraries for translation services

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
