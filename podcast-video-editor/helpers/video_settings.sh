#!/bin/bash

# Video type and basic settings functions

# Global variables that will be set by these functions
SUGGESTED_MODEL=""
SUGGESTED_THRESHOLD=""
SILENCE_DURATION=""

# Ask about video type and content
get_video_type() {
    print_header "Video Type & Content"

    echo "What type of video are you processing?"
    echo "1) Podcast episode"
    echo "2) Interview/Conversation"
    echo "3) Educational lecture/presentation"
    echo "4) Meeting recording"
    echo "5) Other (custom settings)"
    echo ""

    while true; do
        read -p "Select video type (1-5): " video_type

        case $video_type in
            1)
                print_info "Podcast episode selected"
                SUGGESTED_MODEL="base"
                SUGGESTED_THRESHOLD="-40"
                SILENCE_DURATION="0.5"
                break
                ;;
            2)
                print_info "Interview/Conversation selected"
                SUGGESTED_MODEL="small"
                SUGGESTED_THRESHOLD="-35"
                SILENCE_DURATION="0.8"
                break
                ;;
            3)
                print_info "Educational lecture selected"
                SUGGESTED_MODEL="medium"
                SUGGESTED_THRESHOLD="-45"
                SILENCE_DURATION="1.0"
                break
                ;;
            4)
                print_info "Meeting recording selected"
                SUGGESTED_MODEL="base"
                SUGGESTED_THRESHOLD="-30"
                SILENCE_DURATION="1.5"
                break
                ;;
            5)
                print_info "Custom settings mode"
                SUGGESTED_MODEL="base"
                SUGGESTED_THRESHOLD="-40"
                SILENCE_DURATION="0.5"
                break
                ;;
            *)
                print_error "Please select 1-5"
                ;;
        esac
    done

    echo ""
}
