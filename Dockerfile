FROM osrf/ros:humble-desktop-full

# Colored prompt and ROS source
RUN sed -i 's/#force_color_prompt=yes/force_color_prompt=yes/g' ~/.bashrc && \
    echo "source /opt/ros/$ROS_DISTRO/setup.bash" >> ~/.bashrc

# COPY . /home/ros2_ws/src/unitree_a1_control
WORKDIR /home/ros2_ws