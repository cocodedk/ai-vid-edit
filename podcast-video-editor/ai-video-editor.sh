#!/bin/bash

# AI Video Editor - Interactive Setup Script
# This script guides you through the best settings for your video editing needs

set -e

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --help|-h)
            echo "AI Video Editor - Interactive Setup Script"
            echo ""
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "This interactive script guides you through optimal settings for AI video editing."
            echo ""
            echo "Options:"
            echo "  --help, -h    Show this help message"
            echo "  --version     Show version information"
            echo ""
            echo "The script will ask questions about your video type, language, quality"
            echo "preferences, and generate an optimized command for processing."
            echo ""
            echo "Examples:"
            echo "  $0                    # Start interactive setup"
            echo "  $0 --help            # Show this help"
            echo ""
            exit 0
            ;;
        --version)
            echo "AI Video Editor v1.0.0"
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            echo "Use --help for usage information" >&2
            exit 1
            ;;
    esac
    shift
done

# Load helper scripts
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/helpers/utils.sh"
source "$SCRIPT_DIR/helpers/environment.sh"
source "$SCRIPT_DIR/helpers/video_file.sh"
source "$SCRIPT_DIR/helpers/video_settings.sh"
source "$SCRIPT_DIR/helpers/language_settings.sh"
source "$SCRIPT_DIR/helpers/quality_settings.sh"
source "$SCRIPT_DIR/helpers/output_settings.sh"
source "$SCRIPT_DIR/helpers/preview_settings.sh"
source "$SCRIPT_DIR/helpers/command_generator.sh"
source "$SCRIPT_DIR/helpers/completion.sh"

# Main execution
main() {
    echo ""
    print_header "🤖 AI Video Editor - Interactive Setup"

    check_environment
    get_video_file
    get_video_type
    get_language
    get_quality_preferences
    get_gpu_settings
    get_output_preferences
    get_preview_preference
    generate_command

    print_success "Setup complete! Your video is ready for AI-powered editing."
    echo ""
    echo "Tips for best results:"
    echo "• Use --verbose for detailed progress information"
    echo "• Try preview mode first: podcast-editor preview video.mp4"
    echo "• For long videos, consider using a larger Whisper model"
    echo "• GPU acceleration significantly speeds up processing"
    echo ""
}

# Setup bash completion
setup_completion

# Run the script
main "$@"
