execute_process(COMMAND "/home/robertslab/rl_workspace_0/build/camera_calibration/catkin_generated/python_distutils_install.sh" RESULT_VARIABLE res)

if(NOT res EQUAL 0)
  message(FATAL_ERROR "execute_process(/home/robertslab/rl_workspace_0/build/camera_calibration/catkin_generated/python_distutils_install.sh) returned error code ")
endif()
