#include "ballstorage.h"
#include "buzzer.h"
#include "servo.h"
#include "ssd1306.h"
#include "fonts.h"
#include "arm_controller.h"

volatile uint32_t previousMillis = 0;
volatile uint32_t currentMillis = 0;
volatile uint16_t ballCount = 0;
volatile uint8_t is_rotating = 0;

char pos_1;
char pos_2;
char pos_3;
char pos_4;
char pos_5;



#define TOTAL_SLOTS 5  // Adjust based on the number of ball slots
#define GPIO_ENCODER_PIN GPIO_PIN_3  // Encoder sensor pin

// Interrupt callback function for ball slot counting
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
	currentMillis = HAL_GetTick();
    if (GPIO_Pin == GPIO_ENCODER_PIN && (currentMillis - previousMillis > 650) && is_rotating == 1) {
        ballCount++;
        previousMillis = currentMillis;
    }
}

// Function to rotate the storage to a desired slot position
void rotate_360_to_position(uint8_t desired_position) {
	is_rotating = 1;
	desired_position--;
    uint8_t current_position = get_ball_count();
    if (desired_position == current_position) {
        Stop360Servo();
        return;
    }

    Turn360Servo();

    // Delay start
    uint32_t previousMillis_2 = HAL_GetTick();
    uint32_t currentMillis_2  = HAL_GetTick();
    while (currentMillis_2 - previousMillis_2 < 200) {
        currentMillis_2 = HAL_GetTick();
    }
    previousMillis_2 = currentMillis_2;
    // Delay end
    
    ballCount = current_position; // Ignore the balls counted during the delay
    while (get_ball_count() != desired_position);
    is_rotating = 0;
    Stop360Servo();
}

// Function to get the current slot count based on encoder
uint8_t get_ball_count() {
    return ballCount % TOTAL_SLOTS;
}

// Storing high-level function
void store_ball(uint8_t desired_position, BallColor colour) {
    rotate_360_to_position(desired_position);
    switch (desired_position) {
        case 0:
            pos_1 = colour;
            break;
        case 1:
            pos_2 = colour;
            break;
        case 2:
            pos_3 = colour;
            break;
        case 3:
            pos_4 = colour;
            break;
        case 4:
            pos_5 = colour;
            break;
    }
    pickup_and_Store();
    //HAL_Delay(2000);
    return_home();
}

// Retrieving high-level function
void retrieve_ball(BallColor colour) {
    if (pos_1 == colour) {
        rotate_360_to_position(1);
        HAL_Delay(200);
        retrive_and_drop();
        HAL_Delay(2000);
        return_home();
        pos_1 = NO_BALL;
    }
    if (pos_2 == colour) {
        rotate_360_to_position(2);
        HAL_Delay(200);
        retrive_and_drop();
        HAL_Delay(2000);
        return_home();
        pos_2 = NO_BALL;
    }
    if (pos_3 == colour) {
        rotate_360_to_position(3);
        HAL_Delay(200);
        retrive_and_drop();
        HAL_Delay(2000);
        return_home();
        pos_3 = NO_BALL;
    }
    if (pos_4 == colour) {
        rotate_360_to_position(4);
        HAL_Delay(200);
        retrive_and_drop();
        HAL_Delay(2000);
        return_home();
        pos_4 = NO_BALL;
    }
    if (pos_5 == colour) {
        rotate_360_to_position(5);
        HAL_Delay(200);
        retrive_and_drop();
        HAL_Delay(2000);
        return_home();
        pos_5 = NO_BALL;
    }
}
