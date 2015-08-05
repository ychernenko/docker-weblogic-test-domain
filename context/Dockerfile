FROM ychernenko/weblogic-1036:1.0.0

ENV DOMAIN_SCRIPT=test-domain.wlst.py \
    START_ALL_SCRIPT=startAll.wlst.py \
    NODE_MANAGER=localhost \
    WLST_SCRIPTS_HOME=/home/wlst \
    CONFIG_JVM_ARGS=-Djava.security.egd=file:/dev/./urandom \
    DOMAIN_NAME=test

ENV	DOMAIN_HOME=$BEA_HOME/user_projects/domains/$DOMAIN_NAME \
    PATH=$PATH:$DOMAIN_HOME/bin

COPY $DOMAIN_SCRIPT $START_ALL_SCRIPT $WLST_SCRIPTS_HOME/

RUN wlst.sh $WLST_SCRIPTS_HOME/$DOMAIN_SCRIPT