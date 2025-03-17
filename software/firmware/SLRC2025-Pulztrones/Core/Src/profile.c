#include "profile.h"
#include <math.h>
#include "ssd1306.h"
#include "fonts.h"
#include <stdio.h>

// Reset the profile
void Profile_Reset(Profile *profile) {
    profile->position = 0;
    profile->speed = 0;
    profile->target_speed = 0;
    profile->state = PS_IDLE;
}

//Profile forward_profile = {0};
//Profile rotation_profile = {0};

// Check if the profile has finished
uint8_t Profile_IsFinished(const Profile *profile) {
    return profile->state == PS_FINISHED;
}

// Start a profile
void Profile_Start(Profile *profile, float distance, float top_speed, float final_speed, float acceleration) {
    profile->sign = (distance < 0) ? -1 : 1;
    if (distance < 0) distance = -distance;

    if (distance < 1.0f) {
        profile->state = PS_FINISHED;
        return;
    }

    if (final_speed > top_speed) {
        final_speed = top_speed;
    }

    profile->position = 0;
    profile->final_position = distance;
    profile->target_speed = profile->sign * fabsf(top_speed);
    profile->final_speed = profile->sign * fabsf(final_speed);
    profile->acceleration = fabsf(acceleration);
    profile->one_over_acc = (profile->acceleration >= 1) ? (1.0f / profile->acceleration) : 1.0f;
    profile->state = PS_ACCELERATING;
}

// Move a profile (blocking call)
void Profile_Move(Profile *profile, float distance, float top_speed, float final_speed, float acceleration) {
    Profile_Start(profile, distance, top_speed, final_speed, acceleration);
    Profile_WaitUntilFinished(profile);
}

// Stop the profile
void Profile_Stop(Profile *profile) {
    profile->target_speed = 0;
    Profile_Finish(profile);
}

// Finish the profile
void Profile_Finish(Profile *profile) {
    profile->speed = profile->target_speed;
    profile->state = PS_FINISHED;
}

// Wait until the profile finishes
void Profile_WaitUntilFinished(Profile *profile) {
    while (profile->state != PS_FINISHED) {
        HAL_Delay(2);
    }
}

// Get the braking distance
float Profile_GetBrakingDistance(const Profile *profile) {
    return fabsf(profile->speed * profile->speed - profile->final_speed * profile->final_speed) * 0.5f * profile->one_over_acc;
}

// Get the current position
float Profile_GetPosition(const Profile *profile) {
    return profile->position;
}

// Get the current speed
float Profile_GetSpeed(const Profile *profile) {
    return profile->speed;
}

// Get the current acceleration
float Profile_GetAcceleration(const Profile *profile) {
    return profile->acceleration;
}

// Set the speed
void Profile_SetSpeed(Profile *profile, float speed) {
    profile->speed = speed;
}

// Set the target speed
void Profile_SetTargetSpeed(Profile *profile, float speed) {
    profile->target_speed = speed;
}

// Adjust the position
void Profile_AdjustPosition(Profile *profile, float adjustment) {
    profile->position += adjustment;
}

// Set the position
void Profile_SetPosition(Profile *profile, float position) {
    profile->position = position;
}

// Update the profile
void Profile_Update(Profile *profile) {
    if (profile->state == PS_IDLE) return;

    float delta_v = profile->acceleration * LOOP_INTERVAL;
    float remaining = fabsf(profile->final_position) - fabsf(profile->position);

    if (profile->state == PS_ACCELERATING) {
        if (remaining < Profile_GetBrakingDistance(profile)) {
            profile->state = PS_BRAKING;
            profile->target_speed = (profile->final_speed == 0) ? (profile->sign * 5.0f) : profile->final_speed;
        }
    }

    if (profile->speed < profile->target_speed) {
        profile->speed += delta_v;
        if (profile->speed > profile->target_speed) profile->speed = profile->target_speed;
    } else if (profile->speed > profile->target_speed) {
        profile->speed -= delta_v;
        if (profile->speed < profile->target_speed) profile->speed = profile->target_speed;
    }

    profile->position += profile->speed * LOOP_INTERVAL;

    if (profile->state != PS_FINISHED && remaining < 0.125f) {
        profile->state = PS_FINISHED;
        profile->target_speed = profile->final_speed;
    }

}
