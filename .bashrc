# .bashrc

# User specific aliases and functions

alias l='ls -lha'
alias ..='cd ..'
alias ...='cd ../..'

# Source global definitions
if [ -f /etc/bashrc ]; then
        . /etc/bashrc
fi

# enable color support of ls and also add handy aliases
if [ -x /usr/bin/dircolors ]; then
    eval "`dircolors -b`"
    alias ls='ls --color=auto'
    alias dir='dir --color=auto'
    alias vdir='vdir --color=auto'

    alias grep='grep --color=auto'
    alias fgrep='fgrep --color=auto'
    alias egrep='egrep --color=auto'
fi


export HISTTIMEFORMAT="%F %T "
export HISTCONTROL=$HISTCONTROL${HISTCONTROL+,}ignoreboth
export PROMPT_COMMAND="history -a; history -n;"

shopt -s histappend

alias pscgroup='ps -O cgroup:40 -e'

function cgunfreeze() {
        local group=user_services base=/cgroup/system_controller cgroup=
        local subsys=freezer cmd=THAWED param=freezer.state

        if [ "x${1}" == "x" -o ! -w ${base}/${1}/${param} -a ! -w ${base}/${group}/${1}/${param} ]
        then
                echo "usage: cgunfreeze [basegroup/]subgroup"
                return 255;
        fi

        if [ -w ${base}/${1}/${param} ]
        then
                cgroup=${1}/
        else
                cgroup=${group}/${1}/
        fi

        cgset -r ${param}=${cmd} ${cgroup} && echo "cgroup ${cgroup} successfully unfrozen"
}

function cgfreeze() {
    local group=user_services base=/cgroup/system_controller cgroup=
    local subsys=freezer cmd=FROZEN param=freezer.state

    if [ "x${1}" == "x" -o ! -w ${base}/${1}/${param} -a ! -w ${base}/${group}/${1}/${param} ]
    then
        echo "usage: cgfreeze [basegroup/]subgroup"
        return 255;
    fi

    if [ -w ${base}/${1}/${param} ]
    then
        cgroup=${1}/
    else
        cgroup=${group}/${1}/
    fi

    cgset -r ${param}=${cmd} ${cgroup} && echo "cgroup ${cgroup} successfully frozen"
}

function avgmem() {
    local cmd_group=$1
    if [ "x${cmd_group}" == "x" ]
    then
        echo "usage: avgmem command"
        return 255;
    fi

    ps -eF | grep ${cmd_group} | grep -v grep | awk -v cmd_group=${cmd_group} 'BEGIN {
unit[0]="KiB";
unit[1]="MiB";
unit[2]="GiB";
count=0;
count_tot=0
}
{
sum_procs++;
sum_mem += $6;
sum_mem_tot += $6;

}

END {
while(sum_mem >= 1048576) {
    sum_mem /= 1024;
    count++;
}
while(sum_mem_tot >= 1024) {
    sum_mem_tot /= 1024;
    count_tot++;
}
printf("Approximately memory consumption of %s (%d procs): %.2f %s (total %.2f %s)\n", cmd_group, sum_procs, sum_mem / sum_procs, unit[count],sum_mem_tot, unit[count_tot])
}'
}

