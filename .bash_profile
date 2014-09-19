# .bash_profile

# Get the aliases and functions
if [ -f ~/.bashrc ]; then
        . ~/.bashrc
fi


# shared history between sessions
PROMPT_COMMAND="history -a; history -n;"
export PROMPT_COMMAND

# attach directly to a tmux session if non attached
[ -z "${TMUX}" ] && tmux attach

# unssh implementation
function unssh() {
        local LINE=$1
        local KHOSTS=~/.ssh/known_hosts
        local LN=$(wc -l < ${KHOSTS})
        [ -z ${LINE} ] && return
        [ -x /usr/bin/vim ] || return
        [ -w ${KHOSTS} ] || return
        [ ${LINE} -gt ${LN} ] && return
        /usr/bin/vim +${LINE} -c d -c wq ${KHOSTS}
}

# pwcryptgen
function pwcryptgen ()
{
    local password=${1:-$(dd if=/dev/urandom count=2 2>/dev/null | tr -dc "a-zA-Z0-9" | cut -c1-16)};
    local hash_func=${2:-6};
    local salt=$(dd if=/dev/urandom count=2 2>/dev/null | tr -dc "a-zA-Z0-9/" | cut -c1-16);
    perl -e"print crypt('${password}', '\$${hash_func}\$${salt}'), \"\n\";"
}
# savef
savef() {
        timestamp=`date +\%m\%d\%y_\%H\%M\%S`
        if [ $# -eq 0 ] ; then
            echo "Usage: savef filename_list"
            return 1
        fi
        while [ "$1" != "" ]; do
            fullname=$1
            if [ -f $fullname ] ; then
                dname=`dirname $fullname`
                if [ ! -d ${dname}/old ] ; then
                    echo "creating directory ${dname}/old"
                    mkdir ${dname}/old
                fi
                fname=`basename $fullname`
                echo "copying ${fullname} to ${dname}/old/${fname}.${timestamp}"
                cp ${fullname} ${dname}/old/${fname}.${timestamp}
            else
                echo "${fullname} NOT FOUND"
            fi
            shift
        done
}

# show hostname in tmux-tab
settitle() {
      printf "\033k$1\033\\"
    }

ssh() {
    settitle "$*"
    command ssh "$@"
    settitle "tkcentos6"
}

settitle "tkcentos6"

