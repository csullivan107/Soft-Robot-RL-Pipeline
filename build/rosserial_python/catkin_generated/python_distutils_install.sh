#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/robertslab/rl_workspace_0/src/rosserial/rosserial_python"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/robertslab/rl_workspace_0/install/lib/python2.7/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/robertslab/rl_workspace_0/install/lib/python2.7/dist-packages:/home/robertslab/rl_workspace_0/build/rosserial_python/lib/python2.7/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/robertslab/rl_workspace_0/build/rosserial_python" \
    "/usr/bin/python2" \
    "/home/robertslab/rl_workspace_0/src/rosserial/rosserial_python/setup.py" \
    build --build-base "/home/robertslab/rl_workspace_0/build/rosserial_python" \
    install \
    --root="${DESTDIR-/}" \
    --install-layout=deb --prefix="/home/robertslab/rl_workspace_0/install" --install-scripts="/home/robertslab/rl_workspace_0/install/bin"
