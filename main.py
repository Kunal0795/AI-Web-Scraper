import streamlit as st 
from scrape import scrape_website, split_dom_content, clean_body_content, extract_body_content
from parse import parse_with_ollama

st.title("AI Web Scraper")

url = st.text_input("Enter a Website URL: ")

if st.button("Scrape Site"):
    if url:  # Ensure URL is not empty
        st.write("Scraping the Website")
        result = scrape_website(url)
        st.write(result)
        body_content = extract_body_content(result)
        cleaned_content = clean_body_content(body_content)
        
        st.session_state.dom_content = cleaned_content  # No parentheses here
        
        with st.expander("View DOM Content"):
            st.text_area("DOM Content", cleaned_content, height=300)
    else:
        st.write("Please enter a valid URL.")

if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse? ")
    
    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing The Content")
            
            dom_chunks = split_dom_content(st.session_state.dom_content)
            result = parse_with_ollama(dom_chunks, parse_description)
            if dom_chunks:
                for chunk in dom_chunks:
                    st.write(chunk, result)  # Display each chunk
            else:
                st.write("No content found to parse.")
