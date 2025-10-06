#!/bin/bash

# Bash completion setup functions

# Bash completion function
_ai_video_editor_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    opts="--help -h --version"

    case $prev in
        --help|-h|--version)
            return 0
            ;;
    esac

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

# Setup completion for bash and zsh
setup_completion() {
    # Register completion function for bash
    if [[ -n "$BASH_VERSION" ]]; then
        complete -F _ai_video_editor_completion ai-video-editor.sh
        complete -F _ai_video_editor_completion ./ai-video-editor.sh
    fi

    # For zsh completion (if available)
    if [[ -n "$ZSH_VERSION" ]]; then
        autoload -U bashcompinit && bashcompinit
        complete -F _ai_video_editor_completion ai-video-editor.sh
        complete -F _ai_video_editor_completion ./ai-video-editor.sh
    fi
}
