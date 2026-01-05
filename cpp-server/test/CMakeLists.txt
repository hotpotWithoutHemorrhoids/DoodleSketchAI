# test/CMakeLists.txt
# 自动查找所有 test_*.cpp 文件（每个都应包含 main()）
file(GLOB TEST_SOURCES CONFIGURE_DEPENDS "test_*.cpp")

# 为每个测试源文件创建一个可执行程序
foreach(test_source IN LISTS TEST_SOURCES)
    # 提取文件名（不含路径和扩展名），如 "test_utils"
    get_filename_component(test_name ${test_source} NAME_WE)
    
    # 创建可执行文件
    add_executable(${test_name} ${test_source})
    
    # 链接 src 中的静态库（自动获得头文件路径 + 传递依赖）
    target_link_libraries(${test_name} PRIVATE goodlesketch_core)

    # 标记为 EXCLUDE_FROM_ALL 显式调用时候才编译
    set_target_properties(${test_name} PROPERTIES EXCLUDE_FROM_ALL TRUE)
endforeach()