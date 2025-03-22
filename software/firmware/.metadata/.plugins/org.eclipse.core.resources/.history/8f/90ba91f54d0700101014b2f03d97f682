#include "buzzer.h"
#include "main.h"

// Turn on the buzzer (PC15 high)
void Buzzer_On(void)
{
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_SET);
}

// Turn off the buzzer (PC15 low)
void Buzzer_Off(void)
{
    HAL_GPIO_WritePin(GPIOA, GPIO_PIN_5, GPIO_PIN_RESET);
}

// Toggle the buzzer state with a specified delay
void Buzzer_Toggle(uint32_t delay)
{
    Buzzer_On();
    HAL_Delay(delay);
    Buzzer_Off();
    HAL_Delay(delay);
}

void Buzzer_UniquePattern(void)
{
    // Pattern: Short-Short-Long-Short-Long
    // Total duration: 1000ms (1 second)

    Buzzer_On();
    HAL_Delay(100);  // 100ms on
    Buzzer_Off();
    HAL_Delay(100);  // 100ms off

    Buzzer_On();
    HAL_Delay(100);  // 100ms on
    Buzzer_Off();
    HAL_Delay(100);  // 100ms off

    Buzzer_On();
    HAL_Delay(200);  // 200ms on
    Buzzer_Off();
    HAL_Delay(100);  // 100ms off

    Buzzer_On();
    HAL_Delay(100);  // 100ms on
    Buzzer_Off();
    HAL_Delay(100);  // 100ms off

    Buzzer_On();
    HAL_Delay(200);  // 200ms on
    Buzzer_Off();
    // No delay at the end to make it exactly 1 second
}
