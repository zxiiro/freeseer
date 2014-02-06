cmake_minimum_required(VERSION 2.8.9)

set (App_Name "freeseer")
if (App_Name STREQUAL "")
    message(FATAL_ERROR "You must set an App Name")
endif()


project(freeseer)


# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Instruct CMake to run moc automatically when needed.
set(CMAKE_AUTOMOC ON)


# Tell CMake to create the helloworld executable
add_executable(freeseer src/main.cpp)


###
### Find 3rd Party libraries
###

set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/cmake/")


find_package(Qt5Widgets)
qt5_use_modules(freeseer Widgets)


find_package(GStreamer)
if (NOT GSTREAMER_FOUND)
    message (FATAL_ERROR "GStreamer not found!")
endif (NOT GSTREAMER_FOUND)


find_package(GObject)
if (NOT GOBJECT_FOUND)
    message (FATAL_ERROR "GObject not found!")
endif (NOT GOBJECT_FOUND)


find_package(GLIB)
if (NOT GSTREAMER_FOUND)
    message (FATAL_ERROR "GStreamer not found!")
endif (NOT GSTREAMER_FOUND)


include_directories(
    ${GSTREAMER_INCLUDE_DIRS}
    ${GSTREAMER_BASE_INCLUDE_DIRS}
    ${GOBJECT_INCLUDE_DIR}
    ${GLIB_INCLUDE_DIRS}
    ${INCLUDE_DIRECTORIES}
    )

target_link_libraries(${App_Name}
    ${GSTREAMER_LIBRARIES}
    ${GSTREAMER_BASE_LIBRARIES}
    ${GOBJECT_LIBRARIES}
    ${GLIB_LIBRARIES}
    ${TARGET_LINK_LIBRARIES}
    )
