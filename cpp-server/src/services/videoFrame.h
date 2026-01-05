#include <vector>
#include <filesystem>
#include <opencv2/opencv.hpp>


std::vector<cv::Mat> getFrameFromVideo(
        const std::string& video_path, 
        const std::vector<double>& timeList);