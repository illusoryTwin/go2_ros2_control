// #include <rclcpp/rclcpp.hpp>
// #include <control_input_msgs/msg/inputs.hpp>

// class PathCommand : public rclcpp::Node {
// public:
//     PathCommand() : Node("path_command_node") {
//         publisher_ = create_publisher<control_input_msgs::msg::Inputs>("control_input", 10);
//         RCLCPP_INFO(get_logger(), "PathCommand node started.");
//     }

//     void publish_constant_command() {
//         control_input_msgs::msg::Inputs input;
//         input.command = 2;   // Constant command
//         input.rx = 0.5;      // Constant angular velocity
//         input.ry = 0.0;
//         input.lx = 0.0;
//         input.ly = 0.0;

//         RCLCPP_INFO(this->get_logger(), "Publishing constant command: %d", input.command);
//         publisher_->publish(input);
//     }

// private:
//     rclcpp::Publisher<control_input_msgs::msg::Inputs>::SharedPtr publisher_;
// };

// int main(int argc, char *argv[]) {
//     rclcpp::init(argc, argv);
//     auto node = std::make_shared<PathCommand>();

//     // Publish the command once
//     node->publish_constant_command();

//     // Spin briefly to make sure the message is sent out
//     rclcpp::spin_some(node);

//     rclcpp::shutdown();
//     return 0;
// }





#include <rclcpp/rclcpp.hpp>
#include <control_input_msgs/msg/inputs.hpp>
#include <thread>
#include <chrono>

class PathCommand : public rclcpp::Node {
public:
    PathCommand() : Node("path_command_node") {
        publisher_ = create_publisher<control_input_msgs::msg::Inputs>("control_input", 10);
        RCLCPP_INFO(get_logger(), "PathCommand node started.");
    }

    void publish_command(int cmd, float rx = 0.0, float ry = 0.0, float lx = 0.0, float ly = 0.0) {
        control_input_msgs::msg::Inputs input;
        input.command = cmd;
        input.rx = rx;
        input.ry = ry;
        input.lx = lx;
        input.ly = ly;

        RCLCPP_INFO(this->get_logger(), "Publishing command: %d", input.command);
        publisher_->publish(input);
    }

private:
    rclcpp::Publisher<control_input_msgs::msg::Inputs>::SharedPtr publisher_;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PathCommand>();

    // Fixed down
    node->publish_command(2, 0.0, 0.0, 0.0, 0.0);
    rclcpp::spin_some(node);

    std::this_thread::sleep_for(std::chrono::seconds(3));

    // Fixed stand
    node->publish_command(2, 0.0, 0.0, 0.0, 0.0);
    rclcpp::spin_some(node);

    // Wait for 3 seconds
    std::this_thread::sleep_for(std::chrono::seconds(3));

    // Free stand
    node->publish_command(3, 0.0, 0.0, 0.0, 0.0);
    rclcpp::spin_some(node);

    rclcpp::shutdown();
    return 0;
}





// #include <rclcpp/rclcpp.hpp>
// #include <control_input_msgs/msg/inputs.hpp>

// class PathCommand : public rclcpp::Node {
// public:
//     PathCommand() : Node("path_command_node"), step_(0) {
//         publisher_ = create_publisher<control_input_msgs::msg::Inputs>("control_input", 10);
//         timer_ = create_wall_timer(
//             std::chrono::milliseconds(1000),
//             std::bind(&PathCommand::timer_callback, this)
//         );
//         start_time_ = this->now();

//         RCLCPP_INFO(get_logger(), "PathCommand node started.");
//     }

// private:
//     void timer_callback() {
//         auto elapsed = this->now() - start_time_;
//         control_input_msgs::msg::Inputs input;
 
//         if (elapsed.seconds() < 10.0) {
//             input.command = 2;  // Initial command
//             input.rx = 0.0;
//             input.ry = 0.0;

//             // // Simple movement pattern
//             // switch (step_ / step_size_) {
//             //     case 0: input.ly = fixed_speed_; input.lx = 0.0; break;  // Forward
//             //     case 1: input.ly = 0.0; input.lx = fixed_speed_; break;  // Right
//             //     case 2: input.ly = -fixed_speed_; input.lx = 0.0; break; // Backward
//             //     case 3: input.ly = 0.0; input.lx = -fixed_speed_; break; // Left
//             //     default: step_ = 0; return;
//             // }
//         } else {
//             input.command = 3;   // Switched command
//             input.rx = 0.5;      // Angular velocity
//             input.ry = 0.0;
//             input.lx = 0.0;
//             input.ly = 0.0;
//         }
//         RCLCPP_INFO(this->get_logger(), "command: %d", input.command);

//         publisher_->publish(input);
//         step_++;
//     }

//     rclcpp::Publisher<control_input_msgs::msg::Inputs>::SharedPtr publisher_;
//     rclcpp::TimerBase::SharedPtr timer_;
//     rclcpp::Time start_time_;

//     size_t step_ = 0;
//     const float fixed_speed_ = 0.5;
//     const size_t step_size_ = 50;
// };

// int main(int argc, char *argv[]) {
//     rclcpp::init(argc, argv);
//     auto node = std::make_shared<PathCommand>();
//     rclcpp::spin(node);
//     rclcpp::shutdown();
//     return 0;
// }
