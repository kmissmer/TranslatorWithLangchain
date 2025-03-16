# Imports I used
import os
import streamlit as st
from typing import List, Dict
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()


class ContextAwareTranslator:
    """A translator that provides both translation and contextual information for the user."""
    
    def __init__(self, model_name: str = "llama3-8b-8192"):
        # Verify that an API key for Groq is available
        if not os.environ.get("GROQ_API_KEY"):
            st.error("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")
            st.stop()
        
        # Initialize the model
        self.model = ChatGroq(model_name=model_name)
        
        # Available languages
        self.languages = [
            "Spanish", "French", "Italian", "German", "Portuguese", 
            "Chinese", "Japanese", "Korean", "Russian", "Arabic",
            "Dutch", "Swedish", "Greek", "Hindi", "Turkish"
        ]
    
    def get_available_languages(self) -> List[str]:
        """Returns the list of available languages."""
        return self.languages
    
    def create_translation_prompt(self) -> ChatPromptTemplate:
        """Creates a prompt template for translation with context."""
        system_template = """You are a helpful translation assistant. Translate the following text from {source_language} to {target_language}.
        
        After the translation, provide:
        1. A brief cultural context about any idioms or culturally specific references
        2. Any alternate translations that might be more appropriate in different contexts
        3. Pronunciation guide for important or difficult words
        4. Also add a fun fact about penguins! 
        
        """
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", system_template),
            ("user", "{text}")
        ])
        
        return prompt_template
    
    def translate(self, 
                  text: str, 
                  target_language: str, 
                  source_language: str = "English") -> Dict:
        """
        Translate text to the target language and provide contextual information.
        """
        # Validate the target language
        if target_language not in self.languages and target_language != "English":
            supported = ", ".join(self.languages + ["English"])
            raise ValueError(f"Target language '{target_language}' is not supported. Supported languages: {supported}")
        
        # Create the prompt
        prompt = self.create_translation_prompt()
        
        # Format the prompt with the input values
        formatted_prompt = prompt.format_messages(
            source_language=source_language,
            target_language=target_language,
            text=text
        )
        
        # Get the response from the model
        response = self.model.invoke(formatted_prompt)
        
        return {
            "original_text": text,
            "source_language": source_language,
            "target_language": target_language,
            "result": response.content
        }


def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="LangWithLang Translator",
        page_icon="🐧",
        layout="wide"
    )
    
    # Add custom CSS (simplified)
    st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .main-header {
        text-align: center;
        margin-bottom: 2rem;
        color: #0066cc;
    }
    .result-container {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #6c757d;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create layout with columns
    main_cols = st.columns([6, 1])
    
    with main_cols[0]:  # Main content column
        # Header
        st.markdown("<h1 class='main-header'>🐧 LangWithLang Translator</h1>", unsafe_allow_html=True)
        
        # Create an instance of the translator
        translator = ContextAwareTranslator()
        languages = translator.get_available_languages()
        
        # Main area
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Input")
            text_to_translate = st.text_area(
                "Enter text to translate",
                height=150
            )
            
            source_language = st.selectbox(
                "Source Language",
                ["English"] + languages,
                index=0
            )
        
        with col2:
            st.subheader("Output Language")
            target_language = st.selectbox(
                "Target Language",
                languages + ["English"]
            )
            
            # Translation button
            translate_button = st.button("Translate", type="primary", use_container_width=True)
        
        # Processing and results section
        if translate_button:
            if text_to_translate:
                with st.spinner(f"Translating to {target_language}..."):
                    try:
                        # Call the translator
                        translation_result = translator.translate(
                            text=text_to_translate,
                            target_language=target_language,
                            source_language=source_language
                        )
                        
                        # Display the results in a nice format
                        st.markdown("<div class='result-container'>", unsafe_allow_html=True)
                        
                        # Split the result by sections
                        result_text = translation_result["result"]
                        
                        # Display translation result
                        st.subheader("Translation")
                        st.write(result_text)
                        
                        st.markdown("</div>", unsafe_allow_html=True)
                        
                    except Exception as e:
                        st.error(f"Translation error: {str(e)}")
            else:
                st.warning("Please enter text to translate.")
    
    with main_cols[1]:  
        for _ in range(15):
            st.write("")
        
        # Displays Lang the Penguin
        if os.path.isfile("lang_penguin.png"):
            st.image("lang_penguin.png", width=100)
        else:
            st.markdown("<div style='font-size: 60px; text-align: center;'>🐧</div>", unsafe_allow_html=True)
        
        st.markdown("<p style='text-align: center; color: #0066cc; font-weight: bold;'>Lang</p>", unsafe_allow_html=True)
    
    # Sidebar content
    st.sidebar.title("About LangWithLang")
    st.sidebar.info(
        "LangWithLang is your friendly translation companion!"
        "\n\n"
        "This context-aware translator doesn't just translate your text; it provides:"
        "\n\n"
        "- Cultural context for idioms and expressions\n"
        "- Alternative translations for different contexts\n"
        "- Pronunciation guides for important words\n"
        "- It even gives you a fun fact about penguins at the end of every translation!\n\n"
        "Powered by LangChain and Groq's LLaMA3 language model."
    )
    
    # Add Lang the Penguin to sidebar as well
    st.sidebar.markdown("---")
    st.sidebar.markdown("## Meet Lang the Penguin")
    
    if os.path.isfile("Penguin.png"):
        st.sidebar.image("Penguin.png", width=150)
   
    
    st.sidebar.markdown("*Lang the Penguin is here to help with your translations!*")
    
    # Footer
    st.markdown("<div class='footer'>LangWithLang - Created with Streamlit, LangChain, and Groq</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
