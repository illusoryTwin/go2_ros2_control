// #include <rclcpp/rclcpp.hpp>
// #include <control_input_msgs/msg/inputs.hpp>

// class PathCommand : public rclcpp::Node {
// public:
//     PathCommand() : Node("path_command_node"), step_(0) {
//         publisher_ = create_publisher<control_input_msgs::msg::Inputs>("control_input", 10);
//         timer_ = create_wall_timer(
//             std::chrono::milliseconds(100),
//             std::bind(&PathCommand::timer_callback, this)
//         );

//         RCLCPP_INFO(get_logger(), "PathCommand node started.");
//     }

// private:
//     void timer_callback() {
//         control_input_msgs::msg::Inputs input;
//         input.command = 2; // No special command
//         input.rx = 0.0;
//         input.ry = 0.0;

//         // Define a simple path: Forward -> Right -> Backward -> Left
//         switch (step_ / step_size_) {
//             case 0: // Move forward
//                 input.ly = fixed_speed_;
//                 input.lx = 0.0;
//                 break;
//             case 1: // Move right
//                 input.ly = 0.0;
//                 input.lx = fixed_speed_;
//                 break;
//             case 2: // Move backward
//                 input.ly = -fixed_speed_;
//                 input.lx = 0.0;
//                 break;
//             case 3: // Move left
//                 input.ly = 0.0;
//                 input.lx = -fixed_speed_;
//                 break;
//             default:
//                 step_ = 0;
//                 return;
//         }

//         publisher_->publish(input);
//         step_++;
//     }

//     rclcpp::Publisher<control_input_msgs::msg::Inputs>::SharedPtr publisher_;
//     rclcpp::TimerBase::SharedPtr timer_;

//     size_t step_ = 0;
//     const float fixed_speed_ = 0.5;        // Fixed linear speed [-1.0, 1.0]
//     const size_t step_size_ = 50;          // Number of timer ticks per direction
// };

// int main(int argc, char *argv[]) {
//     rclcpp::init(argc, argv);
//     auto node = std::make_shared<PathCommand>();
//     rclcpp::spin(node);
//     rclcpp::shutdown();
//     return 0;
// }


#include <rclcpp/rclcpp.hpp>
#include <control_input_msgs/msg/inputs.hpp>

class PathCommand : public rclcpp::Node {
public:
    PathCommand() : Node("path_command_node"), step_(0) {
        publisher_ = create_publisher<control_input_msgs::msg::Inputs>("control_input", 10);
        timer_ = create_wall_timer(
            std::chrono::milliseconds(100),
            std::bind(&PathCommand::timer_callback, this)
        );
        start_time_ = this->now();

        RCLCPP_INFO(get_logger(), "PathCommand node started.");
    }

private:
    void timer_callback() {
        auto elapsed = this->now() - start_time_;
        control_input_msgs::msg::Inputs input;
 
        if (elapsed.seconds() < 10.0) {
            input.command = 2;  // Initial command
            input.rx = 0.0;
            input.ry = 0.0;

            // // Simple movement pattern
            // switch (step_ / step_size_) {
            //     case 0: input.ly = fixed_speed_; input.lx = 0.0; break;  // Forward
            //     case 1: input.ly = 0.0; input.lx = fixed_speed_; break;  // Right
            //     case 2: input.ly = -fixed_speed_; input.lx = 0.0; break; // Backward
            //     case 3: input.ly = 0.0; input.lx = -fixed_speed_; break; // Left
            //     default: step_ = 0; return;
            // }
        } else {
            input.command = 3;   // Switched command
            input.rx = 0.5;      // Angular velocity
            input.ry = 0.0;
            input.lx = 0.0;
            input.ly = 0.0;
        }
        RCLCPP_INFO(this->get_logger(), "command: %d", input.command);

        publisher_->publish(input);
        step_++;
    }

    rclcpp::Publisher<control_input_msgs::msg::Inputs>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::Time start_time_;

    size_t step_ = 0;
    const float fixed_speed_ = 0.5;
    const size_t step_size_ = 50;
};

int main(int argc, char *argv[]) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<PathCommand>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
