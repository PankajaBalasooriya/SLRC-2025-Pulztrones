#ifndef MOTION_H
#define MOTION_H

#include "stm32f4xx_hal.h"
#include "motors.h"
#include "profile.h"
#include "encoders.h"
#include "controller.h"

extern Profile forward;
extern Profile rotation;
extern Controller controller;

/**
* The Motion class handles high-level locomotion tasks for the robot.
*/
typedef struct {
    Controller controller;
    Profile forward;
    Profile rotation;
} Motion;

/**
* Function prototypes for Motion
*/
void Motion_Init(Motion *motion, Controller *controller, Profile *forward, Profile *rotation);
void Motion_ResetDriveSystem(Motion *motion);

void Motion_Stop(Motion *motion);
void Motion_DisableDrive(Motion *motion);
float Motion_Position(Motion *motion);
float Motion_Velocity(Motion *motion);
float Motion_Acceleration(Motion *motion);
void Motion_SetTargetVelocity(Motion *motion, float velocity);
float Motion_Angle(Motion *motion);
float Motion_Omega(Motion *motion);
float Motion_Alpha(Motion *motion);

void Motion_StartMove(Motion *motion, float distance, float top_speed, float final_speed, float acceleration);
uint8_t Motion_MoveFinished(Motion *motion);
void Motion_Move(Motion *motion, float distance, float top_speed, float final_speed, float acceleration);
void Motion_StartTurn(Motion *motion, float angle, float omega, float alpha);
uint8_t Motion_TurnFinished(Motion *motion);
void Motion_Turn(Motion *motion, float angle, float omega, float alpha);
void Motion_Update(Motion *motion);
void Motion_SetPosition(Motion *motion, float position);
void Motion_AdjustForwardPosition(Motion *motion, float delta);
void Motion_SpinTurn(Motion *motion, float angle, float omega, float alpha);
void Motion_StopAt(Motion *motion, float position);
void Motion_StopAfter(Motion *motion, float distance);
void Motion_WaitUntilPosition(Motion *motion, float position);
void Motion_WaitUntilDistance(Motion *motion, float distance);
void Motion_Turn_(Motion *motion, float angle, float omega, float final_speed, float alpha);

#endif
