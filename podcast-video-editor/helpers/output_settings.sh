#!/bin/bash

# Output settings functions

# Global variables that will be set by these functions
OUTPUT_FILE=""

# Ask about output preferences
get_output_preferences() {
    print_header "Output Settings"

    read -p "Enter output filename (leave empty for auto-generated): " custom_output

    if [[ -z "$custom_output" ]]; then
        OUTPUT_FILE=""
        print_info "Output will be auto-generated inside the run folder as input_filename_edited.mp4"
    else
        OUTPUT_FILE="$custom_output"
        print_info "Custom output file: $custom_output"
    fi

    echo ""
}
