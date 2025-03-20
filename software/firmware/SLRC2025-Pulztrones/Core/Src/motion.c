#include "motion.h"
#include "ssd1306.h"
#include "fonts.h"
#include <stdio.h>
#include "uartcom.h"
#include "encoders.h"

extern UART_HandleTypeDef huart6;

void Motion_Init(Motion *motion, Controller *controller, Profile *forward, Profile *rotation) {
    motion->controller = *controller;  // Copy the controller structure
    motion->forward = *forward;        // Copy the forward profile structure
    motion->rotation = *rotation;      // Copy the rotation profile structure
}

void Motion_ResetDriveSystem(Motion *motion) {
	Motion_Stop(motion);
	Motion_DisableDrive(motion);
    resetEncoders();
    Profile_Reset(&(motion->forward));
    Profile_Reset(&(motion->rotation));
    Controller_ResetControllers(&(motion->controller));
    Controller_EnableControllers(&(motion->controller));
}

void Motion_Stop(Motion *motion) {
	Controller_Stop();
}

void Motion_DisableDrive(Motion *motion) {
	Controller_DisableControllers(&(motion->controller));
}

float Motion_Position(Motion *motion) {
    return Profile_GetPosition(&(motion->forward));
}

float Motion_Velocity(Motion *motion) {
    return Profile_GetSpeed(&(motion->forward));
}

float Motion_Acceleration(Motion *motion) {
    return Profile_GetAcceleration(&(motion->forward));
}

void Motion_SetTargetVelocity(Motion *motion, float velocity) {
    Profile_SetTargetSpeed(&(motion->forward), velocity);
}

float Motion_Angle(Motion *motion) {
    return Profile_GetPosition(&(motion->rotation));
}

float Motion_Omega(Motion *motion) {
    return Profile_GetSpeed(&(motion->rotation));
}

float Motion_Alpha(Motion *motion) {
    return Profile_GetAcceleration(&(motion->rotation));
}


void Motion_StartMove(Motion *motion, float distance, float top_speed, float final_speed, float acceleration) {
    Profile_Start(&(motion->forward), distance, top_speed, final_speed, acceleration);
}

uint8_t Motion_MoveFinished(Motion *motion) {
    return Profile_IsFinished(&(motion->forward));
}

// wait untill mition is completed
void Motion_Move(Motion *motion, float distance, float top_speed, float final_speed, float acceleration) {
    Profile_Move(&(motion->forward), distance, top_speed, final_speed, acceleration);
}

void Motion_StartTurn(Motion *motion, float angle, float omega, float alpha) {
    Profile_Start(&(motion->rotation), angle, omega, 0, alpha);
}

uint8_t Motion_TurnFinished(Motion *motion) {
    return Profile_IsFinished(&(motion->rotation));
}

//wait untill motion is finished
void Motion_Turn(Motion *motion, float angle, float omega, float alpha) {
    Profile_Move(&(motion->rotation), angle, omega, 0, alpha);
}


void Motion_SetPosition(Motion *motion, float position) {
    Profile_SetPosition(&(motion->forward), position);
}

void Motion_AdjustForwardPosition(Motion *motion, float delta) {
    Profile_AdjustPosition(&(motion->forward), delta);
}

void Motion_Turn_(Motion *motion, float angle, float omega, float final_speed, float alpha){
	Profile_Move(&(motion->rotation), angle, omega, final_speed, alpha);
}

void Motion_Update(Motion *motion) {
    Profile_Update(&(motion->forward));
    Profile_Update(&(motion->rotation));
    //UART_Transmit_Float(&huart6, ">V", motion->forward.speed, 2);
    //UART_Transmit_Float(&huart6, ">W", robot_speed(), 2);
}

/**
  *
  * @brief turn in place. Force forward speed to zero
  */
void Motion_SpinTurn(Motion *motion, float angle, float omega, float alpha) {
    Profile_SetTargetSpeed(&(motion->forward), 0);
    while (Profile_GetSpeed(&(motion->forward)) != 0) {
        HAL_Delay(2);
    }
    Motion_Turn(motion, angle, omega, alpha);
}

//***************************************************************************//
 /**
  * These are examples of ways to use the motion control functions
  */

 /**
  * The robot is assumed to be moving. This call will stop at a specific
  * distance. Clearly, there must be enough distance remaining for it to
  * brake to a halt.
  *
  * The current values for speed and acceleration are used.
  *
  * Calling this with the robot stationary is undefined. Don't do that.
  *
  * @brief bring the robot to a halt at a specific distance
  */
void Motion_StopAt(Motion *motion, float position) {
    float remaining = position - Profile_GetPosition(&(motion->forward));
    Profile_Move(&(motion->forward), remaining, Profile_GetSpeed(&(motion->forward)), 0, Profile_GetAcceleration(&(motion->forward)));
}

/**
   * The robot is assumed to be moving. This call will stop  after a
   * specific distance has been travelled
   *
   * Clearly, there must be enough distance remaining for it to
   * brake to a halt.
   *
   * The current values for speed and acceleration are used.
   *
   * Calling this with the robot stationary is undefined. Don't do that.
   *
   * @brief bring the robot to a halt after a specific distance
   */
void Motion_StopAfter(Motion *motion, float distance) {
    Profile_Move(&(motion->forward), distance, Profile_GetSpeed(&(motion->forward)), 0, Profile_GetAcceleration(&(motion->forward)));
}

// Test
void Motion_SwitchToNextMotionAfter(Motion *motion, float distance){
	Profile_Move(&(motion->forward), distance, Profile_GetSpeed(&(motion->forward)), Profile_GetSpeed(&(motion->forward)), Profile_GetAcceleration(&(motion->forward)));
}

/**
 * The robot is assumed to be moving. This utility function call will just
 * do a busy-wait until the forward profile gets to the supplied position.
 *
 * @brief wait until the given position is reached
 */
void Motion_WaitUntilPosition(Motion *motion, float position) {
    while (Profile_GetPosition(&(motion->forward)) < position) {
        HAL_Delay(2);
    }
}

/**
   * The robot is assumed to be moving. This utility function call will just
   * do a busy-wait until the forward profile has moved by the given distance.
   *
   * @brief wait until the given distance has been travelled
   */
void Motion_WaitUntilDistance(Motion *motion, float distance) {
    float target = Profile_GetPosition(&(motion->forward)) + distance;
    Motion_WaitUntilPosition(motion, target);
}


