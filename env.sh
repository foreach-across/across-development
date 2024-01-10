echo "Warning: Across is still using old maven plugins that are not multi-thread safe"

alias mi='mvn install'
alias mci='mvn clean install'
# TODO: add -T1C when multi-thread issue is fixed:
alias miwt='mvn install -DskipTests -Djacoco.skip=true'
alias mciwt='mvn clean install -DskipTests -Djacoco.skip=true'

export JAVA8_HOME=~/.jdks/1.8
export JAVA11_HOME=~/.jdks/11
export JAVA17_HOME=~/.jdks/17
export JAVA21_HOME=~/.jdks/21

export JAVA_HOME=$JAVA8_HOME
export PATH=$JAVA_HOME/bin:$PATH

export ACROSS_DEV_DIR
if [[ -f data-across.yml ]]
then
    ACROSS_DEV_DIR=$(realpath "$PWD")
elif [[ -f ../data-across.yml ]]
then
    ACROSS_DEV_DIR=$(realpath "$PWD"/..)
fi

if [[ -z "$ACROSS_DEV_DIR"  ]]
then
    echo 'Warning: Could not determine ACROSS_DEV_DIR!'
else
    export PATH=$ACROSS_DEV_DIR/bin:$PATH
fi

alias axitest='mvn --fail-at-end --batch-mode clean test-compile failsafe:integration-test failsafe:verify -Dmaven.javadoc.skip=true'

# TestNumericFormElementConfiguration
export LC_MONETARY="nl_BE.UTF-8"
export LC_NUMERIC="nl_BE.UTF-8"

# TestDateTimeFormElementConfiguration
export LC_TIME="en_US.UTF-8"
