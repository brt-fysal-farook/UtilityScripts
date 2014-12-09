GREEN="\[\033[0;32m\]"
NO_COLOUR="\[\033[0m\]"
RED="\[\033[0;31m\]"
YELLOW="\[\033[0;33m\]"

function parse_git_branch () {
    branch=$(git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/\1/')
    tput sgr0
    tput setaf 7
    if [ "$branch" = "master" -o "$branch" = "trunk" ];
    then
        tput bold
        tput setab 1
    elif [[ $branch ]]
    then
        tput setab 2
        branch="⑆ $branch"
    fi
    echo -n $branch
}

function show_status_bubble() {
    gyp_variables=($GYP_GENERATOR_FLAGS)
    gyp_variables+=($GYP_DEFINES)
    status_bubble=()
    for element in "${gyp_variables[@]}"
    do 
        keyValuePair=(${element//=/ })
        key=${keyValuePair[0]}; 
        value=${keyValuePair[1]};
        case $key in
            "clang" )
                if [[ $((value)) == 1 ]]
                then
                    status_bubble+=("clang")
                else
                    status_bubble+=("gcc")
                fi;;

            "OS" | "component" | "output_dir" )
                status_bubble+=("$value");;

            "fastbuild" )
                status_bubble+=("fastbuild@$value");;
        esac
    done
    length=${#status_bubble[@]}
    for i in "${!status_bubble[@]}"
    do
        tput setaf 7
        tput setab 4
        echo -n "${status_bubble[i]}"
        tput sgr0
        if [[ $i == $((length-1)) ]]
        then
            echo -n ""
        else
            echo -n " "
        fi
    done
}
# The below line will intercept every command and set it as the title.
trap 'echo -ne "\e]0;"; echo -n $BASH_COMMAND; echo -ne "\007"' DEBUG
PS1="$GREEN\u $YELLOW\w \$(parse_git_branch)$NO_COLOUR \$(show_status_bubble)$GREEN \$(date +\"%d:%m:%y %T.%3N\")$NO_COLOUR\n\$ "
