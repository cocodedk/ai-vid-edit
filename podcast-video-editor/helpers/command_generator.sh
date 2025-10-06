#!/bin/bash

# Command generation and execution functions

# Generate and display the command
generate_command() {
    print_header "Generated Command"

    # Build shared flags
    LANG_FLAG=""
    if [[ -n "$SELECTED_LANGUAGE" ]]; then
        LANG_FLAG="--language $SELECTED_LANGUAGE"
    fi

    # Build output flag
    OUTPUT_FLAG=""
    if [[ -n "$OUTPUT_FILE" ]]; then
        OUTPUT_FLAG="--output \"$OUTPUT_FILE\""
    fi

    # Preview command (optional)
    PREVIEW_CMD=""
    if [[ "$RUN_PREVIEW" == "true" ]]; then
        PREVIEW_CMD="podcast-editor preview \"$VIDEO_FILE\""

        PREVIEW_CMD+=" --whisper-model $FINAL_MODEL"

        if [[ -n "$LANG_FLAG" ]]; then
            PREVIEW_CMD+=" $LANG_FLAG"
        fi

        if [[ -n "$GPU_FLAG" ]]; then
            PREVIEW_CMD+=" $GPU_FLAG"
        fi

        PREVIEW_CMD+=" --verbose"
    fi

    # Generate the final processing command incrementally to avoid extra spaces
    CMD="podcast-editor process \"$VIDEO_FILE\""

    if [[ -n "$OUTPUT_FLAG" ]]; then
        CMD+=" $OUTPUT_FLAG"
    fi

    CMD+=" --whisper-model $FINAL_MODEL"

    if [[ -n "$LANG_FLAG" ]]; then
        CMD+=" $LANG_FLAG"
    fi

    if [[ -n "$GPU_FLAG" ]]; then
        CMD+=" $GPU_FLAG"
    fi

    CMD+=" --verbose"

    if [[ -n "$PREVIEW_CMD" ]]; then
        echo "Preview command (optional):"
        echo ""
        echo -e "${CYAN}$PREVIEW_CMD${NC}"
        echo ""
        echo "Preview breakdown:"
        echo "  • podcast-editor preview \"$VIDEO_FILE\" - Analyze without exporting"
        echo "  • --whisper-model $FINAL_MODEL - Use $FINAL_MODEL model for analysis"
        if [[ -n "$LANG_FLAG" ]]; then
            echo "  • $LANG_FLAG - Specified language for detection"
        fi
        if [[ -n "$GPU_FLAG" ]]; then
            echo "  • $GPU_FLAG - Selected processing device"
        fi
        echo "  • --verbose - Show detailed progress information"
        echo ""

        read -p "Run the preview command now? (y/n): " run_preview

        if [[ "$run_preview" =~ ^[Yy]$ ]]; then
            print_info "Running preview analysis..."
            echo ""
            eval "$PREVIEW_CMD"
            echo ""
        else
            print_info "Skipping preview execution."
            echo ""
        fi
    fi

    echo "Here's your optimized processing command:"
    echo ""
    echo -e "${CYAN}$CMD${NC}"
    echo ""
    echo "Command breakdown:"
    echo "  • podcast-editor process \"$VIDEO_FILE\" - Process the video file"
    echo "  • --whisper-model $FINAL_MODEL - Use $FINAL_MODEL model for transcription"
    if [[ -n "$LANG_FLAG" ]]; then
        echo "  • $LANG_FLAG - Specified language for better accuracy"
    fi
    if [[ -n "$OUTPUT_FLAG" ]]; then
        echo "  • $OUTPUT_FLAG - Custom output filename"
    fi
    if [[ -n "$GPU_FLAG" ]]; then
        echo "  • $GPU_FLAG - Selected processing device"
    fi
    echo "  • --verbose - Show detailed progress information"
    echo ""

    read -p "Run this command now? (y/n): " run_now

    if [[ "$run_now" =~ ^[Yy]$ ]]; then
        print_info "Executing command..."
        echo ""
        eval "$CMD"
    else
        print_info "Command saved. You can run it manually later:"
        echo "$CMD"
    fi
}
