#!/bin/bash

# Video file selection functions

# Global variables that will be set by these functions
VIDEO_FILE=""

sanitize_path_input() {
    local path="$1"

    if [[ ${#path} -ge 2 ]]; then
        local first_char="${path:0:1}"
        local last_char="${path: -1}"

        if [[ "$first_char" == "$last_char" && ( "$first_char" == "\"" || "$first_char" == "'" ) ]]; then
            path="${path:1:-1}"
        fi
    fi

    printf '%s' "$path"
}

# Ask about video file
get_video_file() {
    print_header "Video File Selection"

    while true; do
        echo "Please provide the path to your video file:"
        echo ""
        read -r -p "Video file path: " video_file
        video_file="$(sanitize_path_input "$video_file")"

        # Check if file exists
        if [[ -f "$video_file" ]]; then
            # Get video info (with timeout to prevent hanging)
            duration=$(get_video_duration "$video_file")

            if [[ -n "$duration" ]]; then
                print_info "Video duration: ${duration}s"
            else
                print_warning "Could not determine video duration (this is normal for some formats)"
            fi
            break
        fi

        print_error "File not found: $video_file"
        echo ""
        echo "Troubleshooting tips:"
        echo "• Make sure the video file exists"
        echo "• Try dragging the file again"
        echo "• Check if the file is in the uploads/ directory"
        echo "• Use the full path if the file is elsewhere"
        echo ""
        echo "Common video formats: .mp4, .mov, .avi, .mkv"
    done

    echo ""
    VIDEO_FILE="$video_file"
}
