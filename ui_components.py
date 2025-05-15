import streamlit as st
from config import DIALECT_EXAMPLES, DEFAULT_ENGLISH_EXAMPLE
import os

def render_sidebar(metadata, files):
    """Render the sidebar with file listings and filters."""
    st.sidebar.header("Saved Speech Files")
    
    # Filter by engine
    engine_filter = st.sidebar.radio(
        "Filter by Engine",
        ["All", "Azure", "ElevenLabs", "Facebook MMS-TTS"],
        index=0
    )
    
    # Filter by dialect
    dialect_options = ["All Dialects"] + list(DIALECT_EXAMPLES.keys())
    dialect_filter = st.sidebar.selectbox("Filter by Dialect", dialect_options)
    
    # Apply filters
    filtered_files = files
    if engine_filter != "All":
        filtered_files = [f for f in filtered_files if f["engine"] == engine_filter]
    
    if dialect_filter != "All Dialects":
        filtered_files = [f for f in filtered_files if "dialect" in f and f["dialect"] == dialect_filter]
    
    # Display files
    st.sidebar.subheader(f"Found {len(filtered_files)} files")
    
    if not filtered_files:
        st.sidebar.info("No audio files found for the selected filters.")
    
    # List files with playback option
    for file in reversed(filtered_files):  # Show newest first
        file_description = f"{file['timestamp']} - {file['engine']}"
        if "dialect" in file:
            file_description += f" ({file['dialect']})"
            
        with st.sidebar.expander(file_description):
            # Show original English text if available
            if "original_text" in file:
                st.write(f"**English:**\n{file['original_text'][:50]}..." if len(file['original_text']) > 50 else file['original_text'])
                st.write(f"**Arabic:**\n{file['text'][:50]}..." if len(file['text']) > 50 else file['text'])
            else:
                st.write(file['text'][:50] + "..." if len(file['text']) > 50 else file['text'])
            
            if file['filepath'] and os.path.exists(file['filepath']):
                st.audio(file['filepath'])
            else:
                st.warning("File not found")

def render_arabic_input_tab(facebook_model, facebook_tokenizer):
    """Render the Arabic Input tab."""
    st.subheader("Arabic Input with Dialect Selection")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Select dialect
        selected_dialect = st.selectbox(
            "Select Arabic Dialect",
            list(DIALECT_EXAMPLES.keys())
        )
        
        # Show example text for the selected dialect
        dialect_text = st.text_area(
            f"Edit {selected_dialect} Text",
            DIALECT_EXAMPLES[selected_dialect],
            height=150
        )
    
    with col2:
        dialect_engine = st.radio(
            "TTS Engine",
            ["Azure", "ElevenLabs", "Facebook MMS-TTS"],
            index=0,
            key="dialect_engine"
        )
        
        # Show dialect comparison
        with st.expander("Compare Dialects"):
            st.markdown("""
            ### Arabic Dialect Variations
            
            The same sentence expressed in different dialects:
            """)
            
            for dialect, example in DIALECT_EXAMPLES.items():
                st.markdown(f"**{dialect}:** {example}")
    
    # Generate speech button
    if st.button("Generate Speech", type="primary", key="dialect_button"):
        with st.spinner(f"Generating {selected_dialect} speech with {dialect_engine}..."):
            filepath = None
            elapsed = 0
            
            if dialect_engine == "Azure":
                from tts_engines import azure_tts
                filepath, elapsed = azure_tts(dialect_text, selected_dialect)
                
            elif dialect_engine == "ElevenLabs":
                from tts_engines import elevenlabs_tts
                filepath, elapsed = elevenlabs_tts(dialect_text, selected_dialect)
                
            else:  # Facebook MMS-TTS
                from tts_engines import facebook_tts
                filepath, elapsed = facebook_tts(dialect_text, facebook_model, facebook_tokenizer, selected_dialect)
                
            if filepath:
                st.audio(filepath)
                st.success(f"Generated {selected_dialect} speech in {elapsed:.2f} seconds")
                st.rerun()  # Refresh sidebar

def render_translation_tab(translation_model, translation_tokenizer, facebook_model, facebook_tokenizer):
    """Render the English-to-Arabic translation tab."""
    st.subheader("English-to-Arabic Translation")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        english_text_input = st.text_area(
            "Enter English Text", 
            DEFAULT_ENGLISH_EXAMPLE,
            height=150
        )
        
        # Add option for dialect translation
        target_dialect = st.selectbox(
            "Target Dialect (optional)",
            ["Modern Standard Arabic"] + [d for d in DIALECT_EXAMPLES.keys() if d != "Modern Standard Arabic"],
            help="Note: Translation initially produces MSA, then is adjusted for dialect characteristics"
        )
    
    with col2:
        translation_engine = st.radio(
            "TTS Engine",
            ["Azure", "ElevenLabs", "Facebook MMS-TTS"],
            index=0,
            key="translation_engine"
        )
    
    # Translate button
    if st.button("Translate and Generate Speech", type="primary", key="translate_button"):
        with st.spinner("Translating English to Arabic..."):
            # Translate the text
            from translation import translate_english_to_arabic
            translated_text = translate_english_to_arabic(english_text_input, translation_model, translation_tokenizer)
            
            if not translated_text:
                st.error("Translation failed. Please try again or enter Arabic text directly.")
                st.stop()
            
            # Show the translated text
            st.subheader("Translated Arabic Text:")
            st.write(translated_text)
            
            # Generate speech with the translated text
            with st.spinner(f"Generating speech with {translation_engine}..."):
                filepath = None
                elapsed = 0
                
                if translation_engine == "Azure":
                    from tts_engines import azure_tts
                    filepath, elapsed = azure_tts(translated_text, target_dialect, english_text_input)
                    
                elif translation_engine == "ElevenLabs":
                    from tts_engines import elevenlabs_tts
                    filepath, elapsed = elevenlabs_tts(translated_text, target_dialect, english_text_input)
                    
                else:  # Facebook MMS-TTS
                    from tts_engines import facebook_tts
                    filepath, elapsed = facebook_tts(translated_text, facebook_model, facebook_tokenizer, target_dialect, english_text_input)
                    
                if filepath:
                    st.audio(filepath)
                    st.success(f"Generated in {elapsed:.2f} seconds")
                    st.rerun()  # Refresh sidebar