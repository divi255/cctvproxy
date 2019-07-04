#!/bin/sh

[ "x$PYTHON3" = "x" ] && PYTHON3=python3

CONFIG=/usr/local/etc/cctv-proxy.yml

while [ $1 ]; do
  key="$1"
  case $key in
    -f)
      shift
      CONFIG=$1
      shift
      ;;
    start|stop|restart|launch)
      CMD=$1
      shift
      ;;
    *)
      CMD=
      shift
      ;;
  esac
done

if [ ! -f ${CONFIG} ]; then
  echo "config ${CONFIG} not found"
  exit 2
fi

PIDFILE=`grep ^pid:\  ${CONFIG} |awk '{ print $1 }'`

if [ "x${PIDFILE}" = "x" ]; then
  PIDFILE=/tmp/cctv-proxy.pid
fi

case $CMD in
  start)
    $PYTHON3 -m cctvproxy.proxy -f ${CONFIG} > /dev/null &
    echo "server started"
    ;;
  stop)
    if [ -f ${PIDFILE} ]; then
      kill -9 `cat ${PIDFILE}` > /dev/null 2>&1
      rm -f ${PIDFILE}
      echo "server stopped"
    fi
    ;;
  restart)
    $0 stop -f ${CONFIG}
    $0 start -f ${CONFIG}
    ;;
  launch)
    $PYTHON3 -m cctvproxy.proxy -f ${CONFIG} -D
    ;;
  *)
    echo "Usage: $0 start|stop|restart|launch [-f config-file]"
    ;;
esac
