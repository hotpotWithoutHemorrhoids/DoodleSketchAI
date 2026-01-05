file(GLOB_RECURSE SRC_SOURCES 
    CONFIGURE_DEPENDS
    "*.cpp"
    "*.cc"
)

# 创建静态库（名字：myproject_core）
add_library(goodlesketch_core STATIC ${SRC_SOURCES})

# 设置头文件搜索路径（PUBLIC：让链接者也能访问 src/ 下的头文件）
target_include_directories(goodlesketch_core PUBLIC
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}>
    $<INSTALL_INTERFACE:include>
)

# ============ 链接第三方库（如果需要） ============
# 如果找到了 OpenCV，则链接（PRIVATE：仅内部使用）
if(OpenCV_FOUND)
    target_link_libraries(goodlesketch_core PUBLIC ${OpenCV_LIBS})
    # 或更现代的写法（推荐）：
    # target_link_libraries(myproject_core PRIVATE OpenCV::OpenCV)
endif()