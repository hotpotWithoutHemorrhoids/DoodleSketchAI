/**
 * DoodleSketchAI C++ 服务端主程序
 * AI驱动的视频简笔画生成服务
 */

#include <iostream>
#include <memory>
#include <string>
#include <vector>
#include <thread>
#include <signal.h>

#include <grpc++/grpc++.h>
#include <opencv2/opencv.hpp>
#include <yaml-cpp/yaml.h>

#include "core/config.h"
#include "core/logger.h"
#include "core/server.h"
#include "services/video_processor.h"
#include "services/ai_processor.h"
#include "utils/signal_handler.h"

// 全局变量
std::unique_ptr<DoodleSketch::Server> g_server;
std::unique_ptr<DoodleSketch::VideoProcessor> g_video_processor;
std::unique_ptr<DoodleSketch::AIProcessor> g_ai_processor;

// 信号处理
void signal_handler(int signal) {
    DoodleSketch::Logger::info("Received signal {}, shutting down gracefully...", signal);
    
    if (g_server) {
        g_server->Shutdown();
    }
    
    if (g_video_processor) {
        g_video_processor->Stop();
    }
    
    if (g_ai_processor) {
        g_ai_processor->Stop();
    }
}

// 打印帮助信息
void print_help(const char* program_name) {
    std::cout << "Usage: " << program_name << " [options]\n"
              << "Options:\n"
              << "  -h, --help              Show this help message\n"
              << "  -p, --port PORT          Server port (default: 50051)\n"
              << "  -c, --config FILE       Configuration file path\n"
              << "  -l, --log-level LEVEL   Log level (debug, info, warn, error)\n"
              << "  -d, --daemon            Run as daemon\n"
              << "  -v, --version           Show version information\n"
              << std::endl;
}

// 打印版本信息
void print_version() {
    std::cout << "DoodleSketchAI C++ Service v" << PROJECT_VERSION << "\n"
              << "Built with AI-powered video sketch generation\n"
              << "Copyright (c) 2024 DoodleSketchAI Team\n"
              << std::endl;
}

// 解析命令行参数
struct CommandLineArgs {
    int port = 50051;
    std::string config_file = "config/config.yaml";
    std::string log_level = "info";
    bool daemon = false;
    bool show_help = false;
    bool show_version = false;
};

CommandLineArgs parse_arguments(int argc, char* argv[]) {
    CommandLineArgs args;
    
    for (int i = 1; i < argc; ++i) {
        std::string arg = argv[i];
        
        if (arg == "-h" || arg == "--help") {
            args.show_help = true;
        } else if (arg == "-v" || arg == "--version") {
            args.show_version = true;
        } else if (arg == "-p" || arg == "--port") {
            if (i + 1 < argc) {
                args.port = std::atoi(argv[++i]);
            }
        } else if (arg == "-c" || arg == "--config") {
            if (i + 1 < argc) {
                args.config_file = argv[++i];
            }
        } else if (arg == "-l" || arg == "--log-level") {
            if (i + 1 < argc) {
                args.log_level = argv[++i];
            }
        } else if (arg == "-d" || arg == "--daemon") {
            args.daemon = true;
        }
    }
    
    return args;
}

// 初始化配置
bool initialize_config(const std::string& config_file, DoodleSketch::Config& config) {
    try {
        if (!config.LoadFromFile(config_file)) {
            std::cerr << "Failed to load config file: " << config_file << std::endl;
            return false;
        }
        
        DoodleSketch::Logger::info("Configuration loaded from {}", config_file);
        return true;
        
    } catch (const std::exception& e) {
        std::cerr << "Error loading config: " << e.what() << std::endl;
        return false;
    }
}

// 初始化日志系统
bool initialize_logging(const std::string& level) {
    try {
        DoodleSketch::Logger::Initialize(level);
        DoodleSketch::Logger::info("Logging system initialized with level: {}", level);
        return true;
        
    } catch (const std::exception& e) {
        std::cerr << "Error initializing logging: " << e.what() << std::endl;
        return false;
    }
}

// 初始化处理器
bool initialize_processors(const DoodleSketch::Config& config) {
    try {
        // 初始化视频处理器
        g_video_processor = std::make_unique<DoodleSketch::VideoProcessor>(config);
        if (!g_video_processor->Initialize()) {
            DoodleSketch::Logger::error("Failed to initialize video processor");
            return false;
        }
        
        // 初始化 AI 处理器
        g_ai_processor = std::make_unique<DoodleSketch::AIProcessor>(config);
        if (!g_ai_processor->Initialize()) {
            DoodleSketch::Logger::error("Failed to initialize AI processor");
            return false;
        }
        
        DoodleSketch::Logger::info("Processors initialized successfully");
        return true;
        
    } catch (const std::exception& e) {
        DoodleSketch::Logger::error("Error initializing processors: {}", e.what());
        return false;
    }
}

// 启动服务器
bool start_server(int port, const DoodleSketch::Config& config) {
    try {
        std::string server_address = "0.0.0.0:" + std::to_string(port);
        
        g_server = std::make_unique<DoodleSketch::Server>(
            server_address,
            *g_video_processor,
            *g_ai_processor
        );
        
        if (!g_server->Start()) {
            DoodleSketch::Logger::error("Failed to start server");
            return false;
        }
        
        DoodleSketch::Logger::info("Server started on {}", server_address);
        return true;
        
    } catch (const std::exception& e) {
        DoodleSketch::Logger::error("Error starting server: {}", e.what());
        return false;
    }
}

// 守护进程化
bool daemonize() {
    pid_t pid = fork();
    
    if (pid < 0) {
        DoodleSketch::Logger::error("Failed to fork process");
        return false;
    }
    
    if (pid > 0) {
        // 父进程退出
        exit(0);
    }
    
    // 子进程继续
    if (setsid() < 0) {
        DoodleSketch::Logger::error("Failed to create new session");
        return false;
    }
    
    // 重定向标准输入输出
    freopen("/dev/null", "r", stdin);
    freopen("/dev/null", "w", stdout);
    freopen("/dev/null", "w", stderr);
    
    DoodleSketch::Logger::info("Process daemonized successfully");
    return true;
}

int main(int argc, char* argv[]) {
    // 解析命令行参数
    CommandLineArgs args = parse_arguments(argc, argv);
    
    // 显示帮助信息
    if (args.show_help) {
        print_help(argv[0]);
        return 0;
    }
    
    // 显示版本信息
    if (args.show_version) {
        print_version();
        return 0;
    }
    
    // 守护进程化
    if (args.daemon) {
        if (!daemonize()) {
            return 1;
        }
    }
    
    // 设置信号处理器
    DoodleSketch::SignalHandler::Setup({
        SIGINT, SIGTERM, SIGQUIT
    }, signal_handler);
    
    try {
        // 初始化日志系统
        if (!initialize_logging(args.log_level)) {
            return 1;
        }
        
        DoodleSketch::Logger::info("Starting DoodleSketchAI C++ Service v{}", PROJECT_VERSION);
        
        // 加载配置
        DoodleSketch::Config config;
        if (!initialize_config(args.config_file, config)) {
            return 1;
        }
        
        // 应用命令行参数覆盖配置
        if (args.port != 50051) {
            config.set_server_port(args.port);
        }
        
        // 初始化处理器
        if (!initialize_processors(config)) {
            return 1;
        }
        
        // 启动服务器
        if (!start_server(config.get_server_port(), config)) {
            return 1;
        }
        
        DoodleSketch::Logger::info("DoodleSketchAI service started successfully");
        
        // 等待服务器关闭
        g_server->Wait();
        
        DoodleSketch::Logger::info("DoodleSketchAI service stopped");
        
    } catch (const std::exception& e) {
        DoodleSketch::Logger::error("Fatal error: {}", e.what());
        return 1;
    }
    
    return 0;
}
