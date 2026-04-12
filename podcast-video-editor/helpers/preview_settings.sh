#!/bin/bash

# Preview configuration functions

RUN_PREVIEW="false"

get_preview_preference() {
    print_header "Preview Option"

    echo "Preview lets you analyze the video without producing an edited file."
    read -r -p "Run a preview analysis before processing? (y/n): " preview_choice

    if [[ "$preview_choice" =~ ^[Yy]$ ]]; then
        RUN_PREVIEW="true"
        print_info "Preview will run before processing."
    else
        RUN_PREVIEW="false"
        print_info "Skipping preview. You can always run 'podcast-editor preview' later."
    fi

    echo ""
}
