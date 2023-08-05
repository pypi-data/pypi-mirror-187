cmake_minimum_required(VERSION 3.21)
project(rollNW VERSION 0.1.0 LANGUAGES CXX C)
set (CMAKE_CXX_STANDARD 20)
include(cmake/Cache.cmake)

option(ROLLNW_PY_BUILD_DOCS "Build documentation" OFF)

# Generate compile_commands.json to make it easier to work with clang based tools
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)
# AppleClang changes visibility to hidden
if(CMAKE_CXX_COMPILER_ID MATCHES ".*Clang" OR CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  add_compile_options(-fvisibility=hidden)
endif()

if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>")

    add_definitions(
        /bigobj
        -D_CRT_SECURE_NO_WARNINGS
        -DUNICODE
        -D_UNICODE
        -D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS # abseil
        -DSTBI_WINDOWS_UTF8 # stbi_image
    )
endif()

if(WIN32)
    add_definitions(-DROLLNW_OS_WINDOWS)
elseif(APPLE)
    add_definitions(-DROLLNW_OS_MACOS)
elseif(UNIX)
    add_definitions(-DROLLNW_OS_LINUX)
else()
    message(FATAL "Unsupported target platform")
endif()

add_subdirectory(external/rollnw)
add_subdirectory(external/pybind11)
add_subdirectory(src)
