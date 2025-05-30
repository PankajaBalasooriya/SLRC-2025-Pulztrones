/**
  ******************************************************************************
  * @file           : pca9685.c
  * @brief          : PCA9685 PWM controller driver implementation
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "pca9685.h"

/* Private variables ---------------------------------------------------------*/
extern I2C_HandleTypeDef hi2c2;  // I2C handle from main.c

/* Function Implementations --------------------------------------------------*/

/**
  * @brief  Set/clear specific bit in a register
  * @param  Register: Register address to modify
  * @param  Bit: Bit position to modify (0-7)
  * @param  Value: Value to set (0 or 1)
  * @retval None
  */
void PCA9685_SetBit(uint8_t Register, uint8_t Bit, uint8_t Value)
{
  uint8_t readValue;
  // Read all 8 bits and set only one bit to 0/1 and write all 8 bits back
  HAL_I2C_Mem_Read(&hi2c2, PCA9685_ADDRESS, Register, 1, &readValue, 1, 10);
  if (Value == 0)
    readValue &= ~(1 << Bit);
  else
    readValue |= (1 << Bit);
  HAL_I2C_Mem_Write(&hi2c2, PCA9685_ADDRESS, Register, 1, &readValue, 1, 10);
  HAL_Delay(1);
}

/**
  * @brief  Set PWM frequency (24Hz to 1526Hz)
  * @param  frequency: Desired PWM frequency in Hz
  * @retval None
  */
void PCA9685_SetPWMFrequency(uint16_t frequency)
{
  uint8_t prescale;

  // Ensure frequency is within valid range
  if(frequency >= 1526)
    prescale = 0x03;  // Maximum frequency (1526Hz)
  else if(frequency <= 24)
    prescale = 0xFF;  // Minimum frequency (24Hz)
  else
    // Calculate prescale value based on 25MHz internal oscillator
    prescale = (uint8_t)(25000000 / (4096 * frequency));

  // Enter sleep mode before changing the frequency
  PCA9685_SetBit(PCA9685_MODE1, PCA9685_MODE1_SLEEP_BIT, 1);

  // Set the prescale value
  HAL_I2C_Mem_Write(&hi2c2, PCA9685_ADDRESS, PCA9685_PRE_SCALE, 1, &prescale, 1, 10);

  // Exit sleep mode
  PCA9685_SetBit(PCA9685_MODE1, PCA9685_MODE1_SLEEP_BIT, 0);

  // Restart all PWM channels
  PCA9685_SetBit(PCA9685_MODE1, PCA9685_MODE1_RESTART_BIT, 1);
}

/**
  * @brief  Initialize PCA9685 with specified frequency
  * @param  frequency: Desired PWM frequency in Hz
  * @retval None
  */
void PCA9685_Init(uint16_t frequency)
{
  // Set desired PWM frequency (usually 50Hz for standard servos)
  PCA9685_SetPWMFrequency(frequency);

  // Enable Auto-Increment for efficient register writing
  PCA9685_SetBit(PCA9685_MODE1, PCA9685_MODE1_AI_BIT, 1);
}

/**
  * @brief  Set PWM on and off times for specific channel
  * @param  Channel: Channel number (0-15)
  * @param  OnTime: Value between 0-4095 for ON time
  * @param  OffTime: Value between 0-4095 for OFF time
  * @retval None
  */
void PCA9685_SetPWM(uint8_t Channel, uint16_t OnTime, uint16_t OffTime)
{
  uint8_t registerAddress;
  uint8_t pwm[4];

  // Calculate register address for the specified channel
  registerAddress = PCA9685_LED0_ON_L + (4 * Channel);

  // Prepare data bytes for ON and OFF times
  pwm[0] = OnTime & 0xFF;         // ON Low byte
  pwm[1] = (OnTime >> 8) & 0xFF;  // ON High byte
  pwm[2] = OffTime & 0xFF;        // OFF Low byte
  pwm[3] = (OffTime >> 8) & 0xFF; // OFF High byte

  // Write all 4 bytes in a single I2C transaction
  HAL_I2C_Mem_Write(&hi2c2, PCA9685_ADDRESS, registerAddress, 1, pwm, 4, 10);
}

/**
  * @brief  Set servo angle for specific channel
  * @param  Channel: Channel number (0-15)
  * @param  Angle: Desired angle (0-180 degrees)
  * @retval None
  */
void PCA9685_SetServoAngle(uint8_t Channel, float Angle)
{
  float pwmValue;

  // Limit angle to 0-180 range
  if (Angle < 0) Angle = 0;
  if (Angle > 180) Angle = 180;

  // Convert angle to PWM value
  // At 50Hz: 0° = 102.4 value (0.5ms), 180° = 511.9 value (2.5ms)
  pwmValue = (Angle * (511.9 - 102.4) / 180.0) + 102.4;

  // Set PWM with calculated value
  PCA9685_SetPWM(Channel, 0, (uint16_t)pwmValue);
}



