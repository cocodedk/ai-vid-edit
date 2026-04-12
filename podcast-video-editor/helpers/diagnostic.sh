#!/bin/bash

# Diagnostic analysis helpers

DIAGNOSTIC_RAN="false"
DIAGNOSTIC_MODEL=""
DIAGNOSTIC_DEVICE=""
DIAGNOSTIC_THRESHOLD=""
DIAGNOSTIC_SILENCE_DURATION=""
DIAGNOSTIC_NOTES=()

format_size() {
    local bytes="$1"
    if [[ -z "$bytes" ]]; then
        echo "Unknown"
        return
    fi

    if command_exists numfmt; then
        numfmt --to=iec --suffix=B "$bytes"
    else
        echo "${bytes}B"
    fi
}

format_duration() {
    local seconds="$1"
    if [[ -z "$seconds" ]]; then
        echo "Unknown"
        return
    fi

    local mins=$((seconds / 60))
    local hrs=$((mins / 60))
    local rem_mins=$((mins % 60))

    if (( hrs > 0 )); then
        printf "%dh %02dm" "$hrs" "$rem_mins"
    else
        printf "%dm" "$mins"
    fi
}

maybe_update_suggestions() {
    if [[ -n "$1" ]]; then
        SUGGESTED_MODEL="$1"
    fi
    if [[ -n "$2" ]]; then
        SUGGESTED_THRESHOLD="$2"
    fi
    if [[ -n "$3" ]]; then
        SILENCE_DURATION="$3"
    fi
}

run_diagnostics() {
    print_header "Diagnostic Analysis"

    read -r -p "Run diagnostics to suggest optimal settings? (y/n): " diag_choice

    if [[ ! "$diag_choice" =~ ^[Yy]$ ]]; then
        print_info "Skipping diagnostics. You can run 'podcast-editor preview' later for manual analysis."
        echo ""
        return
    fi

    if [[ -z "$VIDEO_FILE" || ! -f "$VIDEO_FILE" ]]; then
        print_warning "Video file not available for diagnostics."
        echo ""
        return
    fi

    DIAGNOSTIC_RAN="true"
    local duration_seconds
    duration_seconds=$(get_video_duration "$VIDEO_FILE")
    local human_duration="$(format_duration "$duration_seconds")"

    local file_size_bytes=""
    if command_exists stat; then
        file_size_bytes=$(stat -c %s "$VIDEO_FILE" 2>/dev/null)
        if [[ -z "$file_size_bytes" ]]; then
            file_size_bytes=$(stat -f%z "$VIDEO_FILE" 2>/dev/null)
        fi
    fi
    local human_size="$(format_size "$file_size_bytes")"

    local has_gpu="$(check_gpu_availability)"
    local gpu_memory_mb=""
    local gpu_name=""
    if [[ "$has_gpu" == "true" ]] && command_exists nvidia-smi; then
        gpu_memory_mb=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n1 | tr -dc '0-9')
        gpu_name=$(nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | head -n1)
    fi

    local duration_minutes=0
    if [[ -n "$duration_seconds" ]]; then
        duration_minutes=$((duration_seconds / 60))
    fi

    local recommended_model="base"
    local recommended_threshold="$SUGGESTED_THRESHOLD"
    local recommended_silence="$SILENCE_DURATION"

    if (( duration_minutes >= 90 )); then
        recommended_threshold="-45"
        recommended_silence="1.2"
    elif (( duration_minutes >= 45 )); then
        recommended_threshold="-42"
        recommended_silence="0.9"
    else
        recommended_threshold="-38"
        recommended_silence="0.6"
    fi

    if [[ "$has_gpu" == "true" && -n "$gpu_memory_mb" ]]; then
        local gpu_memory_gb
        gpu_memory_gb=$(awk -v mem="$gpu_memory_mb" 'BEGIN { if (mem > 0) printf "%.1f", mem/1024; }')

        if (( gpu_memory_mb >= 12288 )); then
            recommended_model="large"
        elif (( gpu_memory_mb >= 8192 )); then
            recommended_model="medium"
        elif (( gpu_memory_mb >= 6144 )); then
            recommended_model="small"
        else
            recommended_model="base"
        fi

        DIAGNOSTIC_DEVICE="cuda"
        if [[ -n "$gpu_memory_mb" ]]; then
            local formatted_gpu_mem
            if [[ -n "$gpu_memory_gb" ]]; then
                formatted_gpu_mem="$gpu_memory_gb GiB"
            else
                formatted_gpu_mem="${gpu_memory_mb} MB"
            fi
            DIAGNOSTIC_NOTES+=("GPU detected: ${gpu_name:-NVIDIA GPU} (${formatted_gpu_mem} VRAM)")
        else
            DIAGNOSTIC_NOTES+=("GPU detected: ${gpu_name:-NVIDIA GPU} (VRAM unknown)")
        fi
    else
        if (( duration_minutes >= 60 )); then
            recommended_model="small"
        elif (( duration_minutes >= 30 )); then
            recommended_model="base"
        else
            recommended_model="tiny"
        fi
        DIAGNOSTIC_DEVICE="cpu"
        if [[ "$has_gpu" == "true" ]]; then
            DIAGNOSTIC_NOTES+=("GPU detected but VRAM information unavailable; defaulting to CPU recommendation")
        else
            DIAGNOSTIC_NOTES+=("No NVIDIA GPU detected; CPU processing recommended")
        fi
    fi

    DIAGNOSTIC_MODEL="$recommended_model"
    DIAGNOSTIC_THRESHOLD="$recommended_threshold"
    DIAGNOSTIC_SILENCE_DURATION="$recommended_silence"

    maybe_update_suggestions "$DIAGNOSTIC_MODEL" "$DIAGNOSTIC_THRESHOLD" "$DIAGNOSTIC_SILENCE_DURATION"

    print_info "Video duration: ${human_duration}"
    print_info "File size: ${human_size}"

    if [[ -n "$gpu_name" ]]; then
        print_info "GPU: $gpu_name"
    fi

    print_info "Recommended Whisper model: $DIAGNOSTIC_MODEL"
    print_info "Recommended device: $DIAGNOSTIC_DEVICE"
    print_info "Suggested silence threshold: ${DIAGNOSTIC_THRESHOLD} dB"
    print_info "Suggested minimum silence duration: ${DIAGNOSTIC_SILENCE_DURATION}s"

    if (( duration_minutes >= 45 )); then
        DIAGNOSTIC_NOTES+=("Long recording detected; consider previewing first to validate cuts")
    fi

    if (( duration_minutes > 0 )) && [[ -n "$file_size_bytes" ]]; then
        local bitrate
        bitrate=$(awk -v size="$file_size_bytes" -v duration="${duration_minutes}" 'BEGIN { if (duration > 0) printf "%.1f", (size/1048576)/duration; }')
        if [[ -n "$bitrate" ]]; then
            DIAGNOSTIC_NOTES+=("Approx. data rate: ${bitrate} MB/min")
        fi
    fi

    if (( ${#DIAGNOSTIC_NOTES[@]} > 0 )); then
        echo ""
        print_info "Diagnostic notes:"
        for note in "${DIAGNOSTIC_NOTES[@]}"; do
            echo "  • $note"
        done
    fi

    print_success "Diagnostics complete. Recommendations have been applied as defaults."
    echo ""
}
