# LangWithLang Translator

A context-aware translation tool that not only translates text but also provides cultural context, alternative translations, and pronunciation guides.

## Features

- Translate between multiple languages
- Provides cultural context for idioms and expressions
- Suggests alternative translations for different contexts
- Includes pronunciation guides for important words
- Simple and intuitive user interface
- Meet Lang the Penguin, your translation companion!

## Installation

### Prerequisites

- Python 3.7 or higher
- A Groq API key (sign up at [groq.com](https://groq.com))

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/langwithlang-translator.git
   cd langwithlang-translator
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and add your Groq API key:
   ```
   GROQ_API_KEY=your-groq-api-key-here
   ```

## Running the App

1. Make sure your virtual environment is activated.

2. Run the Streamlit application:
   ```bash
   streamlit run streamlit_translator.py
   ```

3. The application will open in your default web browser at `http://localhost:8501`.

## Usage

1. Enter the text you want to translate in the input field.
2. Select the source language (default is English).
3. Select the target language you want to translate to.
4. Click the "Translate" button.
5. View the translation results, including cultural context, alternative translations, and pronunciation guides.

## Adding Penguin Images

For the full experience, add the following image to your project directory:
- `Penguin.png` 

## Customization

You can customize the application by:
- Modifying the CSS in the `st.markdown` section
- Adding more languages to the `languages` list in the `ContextAwareTranslator` class
- Changing the model by updating the `model_name` parameter in the `ContextAwareTranslator` class


## Acknowledgements

- Powered by [Streamlit](https://streamlit.io/)
- Language model provided by [Groq](https://groq.com/)
- Integrated with [LangChain](https://www.langchain.com/)
