# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Que is a lightweight system tray application for Windows that enables quick text translation using keyboard shortcuts. The application runs in the background and translates selected text when the user presses Ctrl+Q, automatically copying the translated text to the clipboard.

## Development Commands

### Installation and Setup
```bash
# Install dependencies (recommended)
uv sync

# Alternative: Install with pip
pip install -r requirements.txt

# Create configuration file
cp config.example.json config.json
# Edit config.json to add your API keys
```

### Running the Application
```bash
# Run with normal output (recommended)
uv run python main.py

# Run in quiet mode (suppress console output)
uv run python main.py -q
uv run python main.py --quiet

# Alternative: If installed with pip
python main.py
python main.py -q
python main.py --quiet
```

## Architecture

### Core Components

- **main.py**: Entry point containing the main application logic, keyboard hotkey handling, and system tray integration
- **translators/**: Translation provider abstraction layer
  - **base.py**: Abstract `TranslatorProvider` class defining the translation interface
  - **factory.py**: Factory pattern implementation for loading configured translation providers
  - **gemini.py**: Google Gemini API implementation
  - **openai.py**: OpenAI-compatible API implementation (works with OpenAI, Moonshot AI, etc.)

### Key Design Patterns

- **Factory Pattern**: `translators/factory.py` handles provider instantiation based on configuration
- **Abstract Base Class**: `TranslatorProvider` defines the common interface for all translation providers
- **Global Hotkey Handling**: Uses the `keyboard` library to capture Ctrl+Q system-wide
- **System Tray Integration**: Uses `pystray` for background application with menu interface

### Configuration System

The application uses `config.json` for provider configuration:
- Supports multiple translation providers simultaneously
- Selected provider specified by the `provider` field
- Each provider configuration includes API keys, models, and endpoints
- Default target language is Chinese but can be changed via tray menu

### Translation Workflow

1. User selects text and presses Ctrl+Q
2. Application simulates Ctrl+C to copy selected text
3. Text is sent to configured translation provider
4. Translated result is copied to clipboard
5. Original and translated text shown in console (unless in quiet mode)

## Platform Limitations

- **Windows Only**: Due to the `keyboard` library limitations, this application only works on Windows
- **Python 3.7+**: Minimum Python version requirement
- **Internet Connection**: Required for translation API access