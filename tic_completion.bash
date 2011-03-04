_tic_completion() {
    COMPREPLY=()

    # cm.py in the path?
    #/usr/bin/which -s ./cm.py || return 0

    # cm.py in this folder?
    [[ -e ./cm.py ]] || return 0

    local cur="${COMP_WORDS[COMP_CWORD]}"

    tasks=$(./cm.py shortlist)
    COMPREPLY=( $(compgen -W "${tasks}" -- ${cur}) )
}

complete -F _tic_completion ./cm.py
