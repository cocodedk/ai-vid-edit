#!/bin/bash

# Bash/Zsh completion for ai-video-editor.sh
# Source this file to enable autocompletion:
#   source podcast-video-editor/ai-video-editor-completion.sh

_ai_video_editor_completion() {
    local cur opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"

    opts="--help -h --version"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi

    # For the script name itself, suggest common video files if in a directory with videos
    if [[ ${cur} == "" ]] && [[ -d "uploads" ]]; then
        # Suggest video files from uploads directory
        local video_files
        video_files=$(find uploads -maxdepth 1 -type f \( -iname "*.mp4" -o -iname "*.mov" -o -iname "*.avi" -o -iname "*.mkv" \) -exec basename {} \; 2>/dev/null | head -10)
        if [[ -n "$video_files" ]]; then
            COMPREPLY=( $(compgen -W "${video_files}" -- "") )
        fi
    fi
}

# Register completion for different ways to invoke the script
if [[ -n "$BASH_VERSION" ]]; then
    complete -F _ai_video_editor_completion ai-video-editor.sh
    complete -F _ai_video_editor_completion ./ai-video-editor.sh
    complete -F _ai_video_editor_completion podcast-video-editor/ai-video-editor.sh
elif [[ -n "$ZSH_VERSION" ]] && command -v bashcompinit >/dev/null 2>&1; then
    autoload -U bashcompinit && bashcompinit
    complete -F _ai_video_editor_completion ai-video-editor.sh
    complete -F _ai_video_editor_completion ./ai-video-editor.sh
    complete -F _ai_video_editor_completion podcast-video-editor/ai-video-editor.sh
fi

# Show completion status
if [[ -n "$BASH_VERSION" ]]; then
    echo "✅ Bash completion for ai-video-editor.sh enabled!"
    echo "   Try: ./ai-video-editor.sh --<Tab>"
elif [[ -n "$ZSH_VERSION" ]]; then
    echo "✅ Zsh completion for ai-video-editor.sh enabled!"
    echo "   Try: ./ai-video-editor.sh --<Tab>"
else
    echo "ℹ️  Completion setup completed (shell type not detected)"
fi
