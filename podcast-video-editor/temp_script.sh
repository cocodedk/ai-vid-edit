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

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
    echo -e "${PURPLE}$1${NC}"
    echo -e "${PURPLE}═══════════════════════════════════════════════════${NC}"
}

# Check if we're in the right directory
check_environment() {
    print_header "Environment Check"

    # Check if pyproject.toml exists in current directory
    if [[ ! -f "pyproject.toml" ]]; then
        print_info "pyproject.toml not found in current directory - adjusting paths..."
        # Change to the podcast-video-editor directory (where this script is located)
        cd "$(dirname "$0")"
        print_info "Switched to podcast-video-editor directory"

        # Verify we're in the right place
        if [[ ! -f "pyproject.toml" ]]; then
            print_error "pyproject.toml still not found after directory change."
            echo "Please ensure you're running this script from the correct location."
            exit 1
        fi
    fi

    if [[ ! -d ".venv" ]]; then
        print_warning "Virtual environment not found. Installing dependencies..."
        uv sync
        print_success "Dependencies installed successfully!"
    fi

    # Check if tool is installed
    if ! command -v podcast-editor &> /dev/null; then
        print_warning "Podcast editor tool not installed. Installing globally..."
        uv tool install --editable .
        print_success "Tool installed! You can now use 'podcast-editor' commands from anywhere."
    else
        print_success "Podcast editor tool is ready!"
    fi

    echo ""
}

