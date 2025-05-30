/**
  ******************************************************************************
  * @file           : servo.c
  * @brief          : Servo control abstraction implementation
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "servo.h"
#include <string.h>

/* Private variables ---------------------------------------------------------*/
static Servo_t servos[MAX_SERVOS];
static uint8_t servoCount = 0;
static uint8_t isInitialized = 0;

/* Function Implementations --------------------------------------------------*/

/**
  * @brief  Initialize the servo control system
  * @param  frequency: PWM frequency for the servos (typically 50Hz)
  * @retval None
  */
void Servo_Init(uint16_t frequency)
{
    if (isInitialized)
        return;

    // Initialize PCA9685 with the specified frequency
    PCA9685_Init(frequency);

    // Clear the servo array
    memset(servos, 0, sizeof(servos));
    servoCount = 0;
    isInitialized = 1;
}

/**
  * @brief  Register a new servo with the system
  * @param  channel: PCA9685 channel (0-15)
  * @param  name: Optional name for the servo (can be NULL)
  * @param  minAngle: Minimum angle limit (0-180)
  * @param  maxAngle: Maximum angle limit (0-180)
  * @retval int: Servo ID (0 to MAX_SERVOS-1) or -1 if error
  */
int Servo_Register(uint8_t channel, const char* name, float minAngle, float maxAngle, float init_angle)
{
    // Check if initialized
    if (!isInitialized)
        return -1;

    // Check if we've reached maximum servo count
    if (servoCount >= MAX_SERVOS)
        return -1;

    // Check if channel is valid
    if (channel >= MAX_SERVOS)
        return -1;

    // Check if the channel is already in use
    for (int i = 0; i < servoCount; i++) {
        if (servos[i].initialized && servos[i].channel == channel)
            return -1;
    }

    // Validate angle limits
    if (minAngle < SERVO_ANGLE_MIN) minAngle = SERVO_ANGLE_MIN;
    if (maxAngle > SERVO_ANGLE_MAX) maxAngle = SERVO_ANGLE_MAX;
    if (minAngle >= maxAngle) return -1;

    // Register the servo
    int servoId = servoCount;
    servos[servoId].channel = channel;
    servos[servoId].minAngle = minAngle;
    servos[servoId].maxAngle = maxAngle;
    //servos[servoId].currentAngle = (minAngle + maxAngle) / 2.0f;  // Center position
    servos[servoId].currentAngle = init_angle;
    servos[servoId].initialized = 1;

    // Set optional name
    if (name != NULL) {
        strncpy(servos[servoId].name, name, sizeof(servos[servoId].name) - 1);
        servos[servoId].name[sizeof(servos[servoId].name) - 1] = '\0';  // Ensure null termination
    } else {
        snprintf(servos[servoId].name, sizeof(servos[servoId].name), "Servo%d", servoId);
    }

    // Update servo count
    servoCount++;

    // Move servo to center position
    PCA9685_SetServoAngle(channel, servos[servoId].currentAngle);

    return servoId;
}

/**
  * @brief  Set servo position by ID
  * @param  servoId: ID returned from Servo_Register
  * @param  angle: Desired angle in degrees
  * @retval int: 0 if successful, -1 if error
  */
int Servo_SetAngle(int servoId, float angle)
{
    // Check if servo ID is valid
    if (servoId < 0 || servoId >= servoCount || !servos[servoId].initialized)
        return -1;

    // Clamp angle to servo limits
    if (angle < servos[servoId].minAngle)
        angle = servos[servoId].minAngle;
    if (angle > servos[servoId].maxAngle)
        angle = servos[servoId].maxAngle;

    // Update current angle
    servos[servoId].currentAngle = angle;

    // Set servo position
    PCA9685_SetServoAngle(servos[servoId].channel, angle);

    return 0;
}

/**
  * @brief  Set servo position by name
  * @param  name: Name of the servo
  * @param  angle: Desired angle in degrees
  * @retval int: 0 if successful, -1 if error
  */
int Servo_SetAngleByName(const char* name, float angle)
{
    if (name == NULL)
        return -1;

    int servoId = Servo_GetIdByName(name);

    if (servoId >= 0)
        return Servo_SetAngle(servoId, angle);
    else
        return -1;
}

/**
  * @brief  Get current angle of a servo
  * @param  servoId: ID returned from Servo_Register
  * @retval float: Current angle in degrees or -1.0f if error
  */
float Servo_GetAngle(int servoId)
{
    // Check if servo ID is valid
    if (servoId < 0 || servoId >= servoCount || !servos[servoId].initialized)
        return -1.0f;

    return servos[servoId].currentAngle;
}

/**
  * @brief  Get servo ID by name
  * @param  name: Name of the servo
  * @retval int: Servo ID or -1 if not found
  */
int Servo_GetIdByName(const char* name)
{
    if (name == NULL)
        return -1;

    // Search for servo with the given name
    for (int i = 0; i < servoCount; i++) {
        if (servos[i].initialized && strcmp(servos[i].name, name) == 0)
            return i;
    }

    return -1;
}

/**
  * @brief  Reset all servos to center position (90 degrees)
  * @retval None
  */
void Servo_ResetAll(void)
{
    for (int i = 0; i < servoCount; i++) {
        if (servos[i].initialized) {
            float centerAngle = (servos[i].minAngle + servos[i].maxAngle) / 2.0f;
            Servo_SetAngle(i, centerAngle);
            HAL_Delay(10);  // Small delay between movements
        }
    }
}


void Turn360Servo()
{
  float pwmValue;


  pwmValue = 295.00;//299

  // Set PWM with calculated value
  PCA9685_SetPWM(14, 0, (uint16_t)pwmValue);
}

void Stop360Servo()
{
	float pwmValue;


	  pwmValue = 305;

	  // Set PWM with calculated value
	  PCA9685_SetPWM(14, 0, (uint16_t)pwmValue);
}
