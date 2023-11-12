echo "Warning: Across is still using old maven plugins that are not multi-thread safe"

alias mi='mvn install'
alias mci='mvn clean install'
# TODO: add -T1C when multi-thread issue is fixed:
alias miwt='mvn install -DskipTests -Dmaven.javadoc.skip=true -Djacoco.skip=true'
alias mciwt='mvn clean install -DskipTests -Dmaven.javadoc.skip=true -Djacoco.skip=true'

export JAVA8_HOME=~/.jdks/1.8
export JAVA11_HOME=~/.jdks/11
export JAVA17_HOME=~/.jdks/17
export JAVA21_HOME=~/.jdks/21

export JAVA_HOME=$JAVA8_HOME
export PATH=$JAVA_HOME/bin:$PATH

# export PATH=$PWD/tools:$PATH

alias axitest='mvn --fail-at-end --batch-mode clean test-compile failsafe:integration-test failsafe:verify -Dmaven.javadoc.skip=true'
