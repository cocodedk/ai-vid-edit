#!/bin/bash

# Language settings functions

# Global variables that will be set by these functions
SELECTED_LANGUAGE=""

# Ask about language
get_language() {
    print_header "Language Settings"

    echo "Language detection helps ensure accurate transcription."
    echo ""
    echo "Options:"
    echo "1) Auto-detect language (recommended)"
    echo "2) Specify language manually"
    echo ""

    while true; do
        read -p "Choose language option (1-2): " lang_choice

        case $lang_choice in
            1)
                SELECTED_LANGUAGE=""
                print_info "Auto-detection enabled - system will detect language automatically"
                break
                ;;
            2)
                echo ""
                echo "Common language codes:"
                echo "  en (English)    es (Spanish)    fr (French)"
                echo "  de (German)     it (Italian)    pt (Portuguese)"
                echo "  ru (Russian)    ja (Japanese)   ko (Korean)"
                echo "  zh (Chinese)    ar (Arabic)     hi (Hindi)"
                echo "  fa (Persian)    tr (Turkish)    nl (Dutch)"
                echo ""
                read -p "Enter language code (e.g., 'en', 'es', 'fa'): " manual_lang
                SELECTED_LANGUAGE="$manual_lang"
                print_info "Using language: $manual_lang"
                break
                ;;
            *)
                print_error "Please select 1-2"
                ;;
        esac
    done

    echo ""
}
