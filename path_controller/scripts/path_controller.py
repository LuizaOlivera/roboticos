#!/usr/bin/env python3

import rospy
import numpy as np
from geometry_msgs.msg import Twist
from environment import Env

if __name__ == "__main__":
    rospy.init_node("path_controller_node", anonymous=False)

    env = Env()
    state_scan = env.reset()
    action = np.zeros(2)

    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    r = rospy.Rate(5)  # 5Hz

    remaining_targets = env.goal_numbers  # Quantidade de alvos restantes
    collision_count = 0  # Contador de colisões

    reached_goal = False
    avoiding_obstacle = False

    while not rospy.is_shutdown():
        # Verifica se o objetivo atual foi alcançado
        if not reached_goal:
            if avoiding_obstacle or min(state_scan[:20]) < 0.4:
                action[0] = 0.0
                action[1] = 0.0
                avoiding_obstacle = True
            else:
                action[0] = 0.2
                action[1] = 0.0
                avoiding_obstacle = False
        else:
            action[0] = 0.2
            action[1] = 0.0

        state_scan = env.step(action)

        # Verifica colisões e atualiza o contador
        if min(state_scan[:20]) < 0.13:
            collision_count += 1

        # Verifica se o robô atingiu o objetivo e atualiza variáveis
        if reached_goal:
            if min(state_scan[:20]) < 0.20:
                reached_goal = False
                avoiding_obstacle = False
                remaining_targets -= 1
                print("Robô chegou ao alvo atual. Alvos restantes:", remaining_targets)

        # Atualiza a variável reached_goal quando não há mais alvos restantes
        if remaining_targets == 0:
            reached_goal = True

        r.sleep()

    rospy.loginfo("Número de colisões: %s", collision_count)


