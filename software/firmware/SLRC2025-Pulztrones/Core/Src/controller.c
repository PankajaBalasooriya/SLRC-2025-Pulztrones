/*
 * controller.c
 */

#include "main.h"
#include "controller.h"
//#include "pid.h"
#include "encoders.h"
#include "motors.h"
#include "ssd1306.h"
#include "fonts.h"
#include <stdio.h>

static float oldSpeed = 0;

void Controller_Init(Controller *controller) {
    // Initialize motor struct
	controller->forward_error = 0;
	controller->rotational_error = 0;
	controller->previous_forward_error = 0;
	controller->previous_rotational_error = 0;
	controller->velocity = 0;
	controller->omega = 0;
	controller->left_motor_pwm = 0;
	controller->right_motor_pwm = 0;
	controller->controllers_enabled = 1;
	controller->feedforward_enabled = 1;

}

/**
 * Enable motor controllers.
 */
void Controller_EnableControllers(Controller *controller) {
    controller->controllers_enabled = 1;
}

/**
 * Disable motor controllers.
 */
void Controller_DisableControllers(Controller *controller) {
    controller->controllers_enabled = 0;
}

/**
 * Reset the error integrals for both forward and rotational controllers.
 */
void Controller_ResetControllers(Controller *controller) {
    controller->forward_error = 0;
    controller->rotational_error = 0;
    controller->previous_forward_error = 0;
    controller->previous_rotational_error = 0;
}

void Controller_Stop(){
	setMotorLPWM(0);
	setMotorRPWM(0);
}


/**
 * Update motor controllers based on velocity, angular velocity, and steering adjustment.
 */
void UpdateControllers(Controller *controller, float velocity, float omega, float steering_adjustment) {
    float forward_output, rotational_output, left_output, right_output;
    //float left_speed, right_speed, left_ff, right_ff;

    controller->velocity = velocity;
    controller->omega = omega;

    // Forward motion control
    float forward_increment = velocity * LOOP_INTERVAL;//
    controller->forward_error += forward_increment - robot_fwd_change();
    float forward_diff = controller->forward_error - controller->previous_forward_error;
    controller->previous_forward_error = controller->forward_error;
    forward_output = FWD_KP * controller->forward_error + FWD_KD * forward_diff;

    // Rotational control
    float rotational_increment = omega * LOOP_INTERVAL;
    controller->rotational_error += rotational_increment - robot_rot_change();
    controller->rotational_error -= steering_adjustment;
    float rotational_diff = controller->rotational_error - controller->previous_rotational_error;
    controller->previous_rotational_error = controller->rotational_error;
    rotational_output = ROT_KP * controller->rotational_error + ROT_KD * rotational_diff;

    // Combine forward and rotational outputs
    left_output = forward_output - rotational_output;
    right_output = forward_output + rotational_output;

    float tangent_speed = omega * ROBOT_RADIUS * RADIANS_PER_DEGREE;

	float left_speed = velocity - tangent_speed;
	float right_speed = velocity + tangent_speed;

	if (controller->feedforward_enabled) {
		// Feedforward calculation
		left_output += leftFeedForward(left_speed);
		right_output += rightFeedForward(right_speed);
	}

    if (controller->controllers_enabled) {
    	setMotorLPWM(left_output);
        setMotorRPWM(right_output);
    }


}


float leftFeedForward(float speed) {
//  static float oldSpeed = speed;
  float leftFF = speed * SPEED_FF;
  if (speed > 0) {
    leftFF += BIAS_FF;
  } else if (speed < 0) {
    leftFF -= BIAS_FF;
  } else {
    // No bias when the speed is 0
  }
  float acc = (speed - oldSpeed) * LOOP_FREQUENCY;
  oldSpeed = speed;
  float accFF = ACC_FF * acc;
  leftFF += accFF;
  return leftFF;
}

float rightFeedForward(float speed) {
  //static float oldSpeed = speed;
  float rightFF = speed * SPEED_FF;
  if (speed > 0) {
    rightFF += BIAS_FF;
  } else if (speed < 0) {
    rightFF -= BIAS_FF;
  } else {
    // No bias when the speed is 0
  }
  float acc = (speed - oldSpeed) * LOOP_FREQUENCY;
  oldSpeed = speed;
  float accFF = ACC_FF * acc;
  rightFF += accFF;
  return rightFF;
}

