#!/bin/bash

# Quality and performance settings functions

# Global variables that will be set by these functions
FINAL_MODEL=""
GPU_FLAG=""

# Ask about quality preferences
get_quality_preferences() {
    print_header "Quality & Performance Settings"

    echo "Choose your processing priorities:"
    echo "1) Fast processing (smaller model, basic accuracy)"
    echo "2) Balanced (good accuracy and speed)"
    echo "3) Best quality (largest model, highest accuracy)"
    echo "4) Custom settings"
    echo ""

    while true; do
        read -p "Select quality preference (1-4): " quality_choice

        case $quality_choice in
            1)
                FINAL_MODEL="tiny"
                print_info "Fast processing mode: Using 'tiny' model"
                break
                ;;
            2)
                FINAL_MODEL="$SUGGESTED_MODEL"
                print_info "Balanced mode: Using '$SUGGESTED_MODEL' model (recommended)"
                break
                ;;
            3)
                FINAL_MODEL="large"
                print_info "Best quality mode: Using 'large' model (slower but most accurate)"
                break
                ;;
            4)
                echo ""
                echo "Available Whisper models:"
                echo "  tiny  - Fastest, good for testing (39 MB)"
                echo "  base  - Good balance (74 MB)"
                echo "  small - Better accuracy (244 MB)"
                echo "  medium- High accuracy (769 MB)"
                echo "  large - Best accuracy (1550 MB)"
                echo ""
                read -p "Enter model size (tiny/base/small/medium/large): " custom_model
                FINAL_MODEL="$custom_model"
                print_info "Using custom model: $FINAL_MODEL"
                break
                ;;
            *)
                print_error "Please select 1-4"
                ;;
        esac
    done

    echo ""
}

# Ask about GPU usage
get_gpu_settings() {
    print_header "Hardware Acceleration"

    if [[ "$(check_gpu_availability)" == "true" ]]; then
        print_info "NVIDIA GPU detected!"
        echo "GPU acceleration can significantly speed up processing."
        echo ""
        read -p "Use GPU acceleration? (y/n): " use_gpu

        if [[ "$use_gpu" =~ ^[Yy]$ ]]; then
            GPU_FLAG="--device cuda"
            print_info "GPU acceleration enabled"
        else
            GPU_FLAG="--device cpu"
            print_info "Using CPU processing"
        fi
    else
        print_warning "No NVIDIA GPU detected. Processing will use CPU."
        print_info "For faster processing, consider using a GPU-enabled system."
        GPU_FLAG="--device cpu"
    fi

    echo ""
}
