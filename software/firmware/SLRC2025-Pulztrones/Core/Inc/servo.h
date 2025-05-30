/**
  ******************************************************************************
  * @file           : servo.h
  * @brief          : Header file for servo control abstraction
  ******************************************************************************
  */

#ifndef SERVO_H
#define SERVO_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "pca9685.h"
#include <stdio.h>


/* Defines -------------------------------------------------------------------*/
#define MAX_SERVOS           16      // Maximum number of servos supported by PCA9685
#define SERVO_ANGLE_MIN      0.0f    // Minimum servo angle in degrees
#define SERVO_ANGLE_MAX      180.0f  // Maximum servo angle in degrees

/* Servo configuration structure */
typedef struct {
    uint8_t channel;         // PCA9685 channel (0-15)
    float minAngle;          // Minimum angle (degrees)
    float maxAngle;          // Maximum angle (degrees)
    float currentAngle;      // Current angle position
    uint8_t initialized;     // Flag to indicate if this servo is initialized
    char name[16];           // Optional name for the servo
} Servo_t;

/* Function Prototypes -------------------------------------------------------*/
/**
  * @brief  Initialize the servo control system
  * @param  frequency: PWM frequency for the servos (typically 50Hz)
  * @retval None
  */
void Servo_Init(uint16_t frequency);

/**
  * @brief  Register a new servo with the system
  * @param  channel: PCA9685 channel (0-15)
  * @param  name: Optional name for the servo (can be NULL)
  * @param  minAngle: Minimum angle limit (0-180)
  * @param  maxAngle: Maximum angle limit (0-180)
  * @retval int: Servo ID (0 to MAX_SERVOS-1) or -1 if error
  */
int Servo_Register(uint8_t channel, const char* name, float minAngle, float maxAngle,float init_angle);

/**
  * @brief  Set servo position by ID
  * @param  servoId: ID returned from Servo_Register
  * @param  angle: Desired angle in degrees
  * @retval int: 0 if successful, -1 if error
  */
int Servo_SetAngle(int servoId, float angle);

/**
  * @brief  Set servo position by name
  * @param  name: Name of the servo
  * @param  angle: Desired angle in degrees
  * @retval int: 0 if successful, -1 if error
  */
int Servo_SetAngleByName(const char* name, float angle);

/**
  * @brief  Get current angle of a servo
  * @param  servoId: ID returned from Servo_Register
  * @retval float: Current angle in degrees or -1.0f if error
  */
float Servo_GetAngle(int servoId);

/**
  * @brief  Get servo ID by name
  * @param  name: Name of the servo
  * @retval int: Servo ID or -1 if not found
  */
int Servo_GetIdByName(const char* name);

/**
  * @brief  Reset all servos to center position (90 degrees)
  * @retval None
  */
void Servo_ResetAll(void);


void Turn360Servo();

void Stop360Servo();

#ifdef __cplusplus
}
#endif

#endif /* SERVO_H */
