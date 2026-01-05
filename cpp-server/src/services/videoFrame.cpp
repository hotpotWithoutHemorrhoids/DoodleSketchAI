#include "videoFrame.h"
#include <iostream>

namespace fs = std::filesystem;
std::vector<cv::Mat> getFrameFromVideo(const std::string& video_path, const std::vector<double>& timeList)
{
    if(!fs::exists(video_path)){
        std::cout<< "video not exists! "<< std::endl;
        exit(-1);
    }

    cv::VideoCapture cap(video_path);
    if(!cap.isOpened()){
        std::cerr<<"error: can't open video "<<video_path<<std::endl;
        exit(-1);
    }

    double fps = cap.get(cv::CAP_PROP_FPS);
    double total_frame_count = cap.get(cv::CAP_PROP_FRAME_COUNT);
    double duration_sec = total_frame_count / fps; // total duration

    size_t valid_frame_count = 0;
    std::vector<double> useTimeList;
    for (size_t i = 0; i < timeList.size(); i++){
        if(timeList[i] > 1 && timeList[i] < duration_sec - 2){
            valid_frame_count++;
            useTimeList.emplace_back(timeList[i]);
        }
    }
    
    std::vector<cv::Mat> result;
    result.reserve(valid_frame_count);

    for (size_t i = 0; i < useTimeList.size(); i++)
    {
        long target_idx = static_cast<long>(useTimeList[i] * fps);
        cap.set(cv::CAP_PROP_POS_FRAMES, target_idx);
        cv::Mat frame;
        if(!cap.read(frame)){
            std::cout<< "read frame failed "<< useTimeList[i]<< std::endl;
            continue;
        }
        result.emplace_back(frame);
    }
    cap.release();
    return result;
}
