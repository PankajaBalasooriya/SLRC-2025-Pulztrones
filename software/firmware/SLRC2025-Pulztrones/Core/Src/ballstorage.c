#include "ballstorage.h"
#include "buzzer.h"
#include "servo.h"

volatile uint32_t previousMillis = 0;
volatile uint32_t currentMillis = 0;
volatile uint16_t ballCount = 0;

#define TOTAL_SLOTS 5  // Adjust based on the number of ball slots
#define GPIO_ENCODER_PIN GPIO_PIN_3  // Encoder sensor pin

// Interrupt callback function for ball slot counting
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    currentMillis = HAL_GetTick();
    if (GPIO_Pin == GPIO_ENCODER_PIN && (currentMillis - previousMillis > 7500)) {
        ballCount++;
        previousMillis = currentMillis;
    }
}

// Function to rotate the storage to a desired slot position
void rotate_to_position(uint8_t desired_position) {
    uint8_t current_position = get_ball_count();
    
    if (desired_position == current_position) {
        Stop360Servo();
        return;
    }

    Turn360Servo();
    while (get_ball_count() != desired_position);
    Stop360Servo();
}

// Function to get the current slot count based on encoder
uint8_t get_ball_count() {
    return ballCount % TOTAL_SLOTS;
}

