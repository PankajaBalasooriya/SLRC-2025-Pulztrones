/**
  ******************************************************************************
  * @file           : pca9685.h
  * @brief          : Header file for PCA9685 PWM controller driver
  ******************************************************************************
  */

#ifndef PCA9685_H
#define PCA9685_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Defines -------------------------------------------------------------------*/
#define PCA9685_ADDRESS            0x80        // I2C device address
#define PCA9685_MODE1              0x0         // Mode Register 1
#define PCA9685_PRE_SCALE          0xFE        // Prescaler for PWM output frequency
#define PCA9685_LED0_ON_L          0x6         // LED0 ON Low Byte Register
#define PCA9685_MODE1_SLEEP_BIT    4           // Sleep bit in MODE1 register
#define PCA9685_MODE1_AI_BIT       5           // Auto-Increment bit in MODE1 register
#define PCA9685_MODE1_RESTART_BIT  7           // Restart bit in MODE1 register

/* Function Prototypes -------------------------------------------------------*/
/**
  * @brief  Set/clear specific bit in a register
  * @param  Register: Register address to modify
  * @param  Bit: Bit position to modify (0-7)
  * @param  Value: Value to set (0 or 1)
  * @retval None
  */
void PCA9685_SetBit(uint8_t Register, uint8_t Bit, uint8_t Value);

/**
  * @brief  Set PWM frequency (24Hz to 1526Hz)
  * @param  frequency: Desired PWM frequency in Hz
  * @retval None
  */
void PCA9685_SetPWMFrequency(uint16_t frequency);

/**
  * @brief  Initialize PCA9685 with specified frequency
  * @param  frequency: Desired PWM frequency in Hz
  * @retval None
  */
void PCA9685_Init(uint16_t frequency);

/**
  * @brief  Set PWM on and off times for specific channel
  * @param  Channel: Channel number (0-15)
  * @param  OnTime: Value between 0-4095 for ON time
  * @param  OffTime: Value between 0-4095 for OFF time
  * @retval None
  */
void PCA9685_SetPWM(uint8_t Channel, uint16_t OnTime, uint16_t OffTime);

/**
  * @brief  Set servo angle for specific channel
  * @param  Channel: Channel number (0-15)
  * @param  Angle: Desired angle (0-180 degrees)
  * @retval None
  */
void PCA9685_SetServoAngle(uint8_t Channel, float Angle);

#ifdef __cplusplus
}
#endif

#endif /* PCA9685_H */
