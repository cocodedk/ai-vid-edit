#!/bin/bash

# Environment checking and dependency installation functions

# Check if we're in the right directory and set up environment
check_environment() {
    print_header "Environment Check"

    # Check if pyproject.toml exists in current directory
    if [[ ! -f "pyproject.toml" ]]; then
        print_info "pyproject.toml not found in current directory - adjusting paths..."
        # Change to the parent directory (podcast-video-editor directory)
        cd "$(dirname "$0")/.."
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
    if ! command_exists podcast-editor; then
        print_warning "Podcast editor tool not installed. Installing globally..."
        uv tool install --editable .
        print_success "Tool installed! You can now use 'podcast-editor' commands from anywhere."
    else
        print_success "Podcast editor tool is ready!"
    fi

    echo ""
}

# Check if GPU is available
check_gpu_availability() {
    if command_exists nvidia-smi; then
        echo "true"
    else
        echo "false"
    fi
}
