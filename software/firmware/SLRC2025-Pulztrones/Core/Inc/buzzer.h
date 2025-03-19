#ifndef __BUZZER_H
#define __BUZZER_H

#include "stm32f4xx_hal.h"  // Include the HAL header for STM32F4

// Buzzer Control Functions

void Buzzer_On(void);          // Function to turn on the buzzer
void Buzzer_Off(void);         // Function to turn off the buzzer
void Buzzer_Toggle(uint32_t delay); // Toggle buzzer with a delay
void Buzzer_UniquePattern(void);

#endif // __BUZZER_H
