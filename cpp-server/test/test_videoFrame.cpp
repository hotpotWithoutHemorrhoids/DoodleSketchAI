#include "services/videoFrame.h"


namespace fs = std::filesystem;
int main(int argc, char const *argv[])
{
    std::string video_path = "/home/ysm/project/DoodleSketchAI/cpp-server/test/data/1.mp4";
    fs::path path = video_path;
    path.parent_path();
    path.filename();
    auto out_dir = path.filename().stem().string()+"_out";
    fs::path output_dir = path.parent_path() / out_dir;
    if(!fs::exists(output_dir)){
        fs::create_directories(output_dir);
    }

    std::vector<double> time_list = {5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65};
    auto out_frames = getFrameFromVideo(video_path, time_list);
    for (int i = 0; i < out_frames.size(); i++)
    {
        auto filename = std::to_string(i) + ".png";
        auto out_path = output_dir / filename;
        cv::imwrite(out_path, out_frames[i]);
    }
    return 0;
}
