#ifndef PROFILE_H
#define PROFILE_H

#include "stm32f4xx_hal.h"
#include <stdint.h>
#include "config.h"

// Profile States
typedef enum {
    PS_IDLE = 0,
    PS_ACCELERATING = 1,
    PS_BRAKING = 2,
    PS_FINISHED = 3
} ProfileState;

// Profile structure
typedef struct {
    volatile ProfileState state;
    volatile float speed;
    volatile float position;
    int8_t sign;
    float acceleration;
    float one_over_acc;
    float target_speed;
    float final_speed;
    float final_position;
} Profile;

// Declare two global instances
extern Profile forward_profile;
extern Profile rotation_profile;

// Function prototypes
void Profile_Reset(Profile *profile);
uint8_t Profile_IsFinished(const Profile *profile);
void Profile_Start(Profile *profile, float distance, float top_speed, float final_speed, float acceleration);
void Profile_Move(Profile *profile, float distance, float top_speed, float final_speed, float acceleration);
void Profile_Stop(Profile *profile);
void Profile_Finish(Profile *profile);
void Profile_WaitUntilFinished(Profile *profile);
float Profile_GetBrakingDistance(const Profile *profile);
float Profile_GetPosition(const Profile *profile);
float Profile_GetSpeed(const Profile *profile);
float Profile_GetAcceleration(const Profile *profile);
void Profile_SetSpeed(Profile *profile, float speed);
void Profile_SetTargetSpeed(Profile *profile, float speed);
void Profile_AdjustPosition(Profile *profile, float adjustment);
void Profile_SetPosition(Profile *profile, float position);
void Profile_Update(Profile *profile);

#endif // PROFILE_H
