#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>
namespace fs = std::filesystem;
int main() {
    // 输入视频路径
    std::string video_path = "/home/ysm/project/DoodleSketchAI/cpp-server/test/data/1.mp4";  
    std::string  output_dir = "/home/ysm/project/DoodleSketchAI/cpp-server/test/data/out";

    // 目标时间：1分10秒 = 70秒
    double target_time_sec = 10.0;

    // 打开视频
    cv::VideoCapture cap(video_path);
    if (!cap.isOpened()) {
        std::cerr << "错误：无法打开视频文件: " << video_path << std::endl;
        return -1;
    }

    // 获取视频总时长（可选，用于验证）
    double fps = cap.get(cv::CAP_PROP_FPS);
    double frame_count = cap.get(cv::CAP_PROP_FRAME_COUNT);
    double duration_sec = frame_count / fps;
    std::cout << "视频总时长: " << duration_sec << " 秒" << " fps: "<< fps << std::endl;
    std::cout << "目标时间: " << target_time_sec << " 秒" << std::endl;

    if (target_time_sec > duration_sec) {
        std::cerr << "警告：目标时间超过视频总时长！" << std::endl;
        target_time_sec = duration_sec - 0.1; // 回退到最后一帧附近
    }

    // 计算目标帧号（从0开始）
    long target_frame = static_cast<long>(target_time_sec * fps);

    // 设置读取位置（跳转到目标帧附近）
    cap.set(cv::CAP_PROP_POS_FRAMES, target_frame);

    // 读取一帧
    cv::Mat frame;
    if (!cap.read(frame)) {
        std::cerr << "错误：无法读取帧（可能视频损坏或时间越界）" << std::endl;
        cap.release();
        return -1;
    }


    if(!fs::exists(output_dir)){
        fs::create_directories(output_dir);
    }

    // 保存为图片（支持 .jpg / .png 等）
    std::string filename = "extracted_frame.jpg";

    fs::path output_path = fs::path(output_dir) / fs::path(filename);
    std::cout<< "output path: "<< output_path<< std::endl;

    if (cv::imwrite(output_path, frame)) {
        std::cout << "✅ 成功保存帧到: " << output_path << std::endl;
    } else {
        std::cerr << "❌ 保存失败！" << std::endl;
    }

    // 释放资源
    cap.release();
    return 0;
}