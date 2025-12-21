cmake_minimum_required(VERSION 3.16)
project(DoodleSketchAI_CPP VERSION 1.0.0 LANGUAGES CXX)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 编译选项
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -g -O0 -Wall -Wextra -pedantic")
    set(CMAKE_CXX_FLAGS_DEBUG "-g -O0")
else()
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -DNDEBUG")
    set(CMAKE_CXX_FLAGS_RELEASE "-O3 -DNDEBUG")
endif()

# 设置输出目录
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# 查找依赖包
find_package(PkgConfig REQUIRED)
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)

# 查找 gRPC
find_package(gRPC CONFIG REQUIRED)
find_package(gRPC++ CONFIG REQUIRED)
find_package(Protobuf CONFIG REQUIRED)

# 查找 FFmpeg
find_path(FFMPEG_INCLUDE_DIRS libavcodec/avcodec.h)
find_library(FFMPEG_LIBAVCODEC avcodec)
find_library(FFMPEG_LIBAVFORMAT avformat)
find_library(FFMPEG_LIBAVUTIL avutil)
find_library(FFMPEG_LIBSWSCALE swscale)

# 查找 ONNX Runtime
find_library(ONNXRUNTIME_LIB onnxruntime)

# 包含目录
include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}/src
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party
    ${OpenCV_INCLUDE_DIRS}
    ${FFMPEG_INCLUDE_DIRS}
    ${PROTOBUF_INCLUDE_DIRS}
    ${GRPC_INCLUDE_DIRS}
)

# 链接库目录
link_directories(
    ${OpenCV_LIB_DIRS}
    ${CMAKE_CURRENT_SOURCE_DIR}/lib
)

# 生成 protobuf 文件
set(PROTO_FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/proto/doodlesketch.proto
)

foreach(PROTO_FILE ${PROTO_FILES})
    get_filename_component(PROTO_NAME ${PROTO_FILE} NAME_WE)
    
    # 生成 C++ 文件
    set(PROTO_SRCS "${PROTO_SRCS};${CMAKE_CURRENT_BINARY_DIR}/${PROTO_NAME}.pb.cc")
    set(PROTO_HDRS "${PROTO_HDRS};${CMAKE_CURRENT_BINARY_DIR}/${PROTO_NAME}.pb.h")
    set(GRPC_SRCS "${GRPC_SRCS};${CMAKE_CURRENT_BINARY_DIR}/${PROTO_NAME}.grpc.pb.cc")
    set(GRPC_HDRS "${GRPC_HDRS};${CMAKE_CURRENT_BINARY_DIR}/${PROTO_NAME}.grpc.pb.h")
    
    add_custom_command(
        OUTPUT "${PROTO_SRCS}" "${PROTO_HDRS}" "${GRPC_SRCS}" "${GRPC_HDRS}"
        COMMAND ${PROTOBUF_PROTOC_EXECUTABLE}
        ARGS --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
             --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
             -I ${CMAKE_CURRENT_SOURCE_DIR}/proto
             ${PROTO_FILE}
        COMMAND ${GRPC_CPP_PLUGIN}
        ARGS --grpc_out=${CMAKE_CURRENT_BINARY_DIR}
             --cpp_out=${CMAKE_CURRENT_BINARY_DIR}
             -I ${CMAKE_CURRENT_SOURCE_DIR}/proto
             ${PROTO_FILE}
        DEPENDS ${PROTO_FILE}
        COMMENT "Running gRPC compiler on ${PROTO_FILE}"
        VERBATIM
    )
endforeach()

# 源文件
file(GLOB_RECURSE SOURCES 
    "src/*.cpp"
    "src/*.cc"
)

file(GLOB_RECURSE HEADERS
    "src/*.h"
    "src/*.hpp"
)

# 创建可执行文件
add_executable(${PROJECT_NAME}
    ${SOURCES}
    ${HEADERS}
    ${PROTO_SRCS}
    ${GRPC_SRCS}
)

# 链接库
target_link_libraries(${PROJECT_NAME}
    # OpenCV
    ${OpenCV_LIBS}
    
    # FFmpeg
    ${FFMPEG_LIBAVCODEC}
    ${FFMPEG_LIBAVFORMAT}
    ${FFMPEG_LIBAVUTIL}
    ${FFMPEG_LIBSWSCALE}
    
    # gRPC
    gRPC::grpc++
    gRPC::grpc++
    protobuf::libprotobuf
    
    # ONNX Runtime (如果找到)
    ${ONNXRUNTIME_LIB}
    
    # 系统库
    pthread
    dl
)

# 编译定义
target_compile_definitions(${PROJECT_NAME}
    PRIVATE
        PROJECT_VERSION="${PROJECT_VERSION}"
        PROJECT_NAME="${PROJECT_NAME}"
)

# 安装规则
install(TARGETS ${PROJECT_NAME}
    RUNTIME DESTINATION bin
)

# 安装配置文件
install(FILES
    ${CMAKE_CURRENT_SOURCE_DIR}/config/config.yaml
    DESTINATION etc/doodlesketch
)

# 安装模型文件
install(DIRECTORY
    ${CMAKE_CURRENT_SOURCE_DIR}/models
    DESTINATION share/doodlesketch
)

# 测试
enable_testing()
add_subdirectory(tests)

# 打包配置
set(CPACK_PACKAGE_NAME ${PROJECT_NAME})
set(CPACK_PACKAGE_VERSION ${PROJECT_VERSION})
set(CPACK_PACKAGE_DESCRIPTION "AI-powered video sketch generation service")
set(CPACK_PACKAGE_VENDOR "DoodleSketchAI Team")
set(CPACK_GENERATOR "TGZ;DEB;RPM")

include(CPack)

# 代码覆盖率 (Debug 模式)
if(CMAKE_BUILD_TYPE STREQUAL "Debug" AND CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    find_program(GCOV_PATH gcov)
    if(GCOV_PATH)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} --coverage")
        set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} --coverage")
        
        add_custom_target(coverage
            COMMAND lcov --capture --directory . --output-file coverage.info
            COMMAND lcov --remove coverage.info '/usr/*' --output-file coverage.info
            COMMAND genhtml coverage.info --output-directory coverage_report
            WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        )
    endif()
endif()

# 静态分析 (如果找到)
find_program(CLANG_TIDY_PATH clang-tidy)
if(CLANG_TIDY_PATH)
    set(CMAKE_CXX_CLANG_TIDY clang-tidy)
endif()

# 格式化
find_program(CLANG_FORMAT_PATH clang-format)
if(CLANG_FORMAT_PATH)
    add_custom_target(format
        COMMAND ${CLANG_FORMAT_PATH} -i ${SOURCES} ${HEADERS}
        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
        COMMENT "Formatting source code with clang-format"
    )
endif()
