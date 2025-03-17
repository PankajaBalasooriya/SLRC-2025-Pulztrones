/*
 * controller.h
 */

#ifndef INC_CONTROLLER_H_
#define INC_CONTROLLER_H_

#include "main.h"
#include "stm32f4xx_hal.h"
#include "config.h"

typedef struct {
    float forward_error;
    float rotational_error;
    float previous_forward_error;
    float previous_rotational_error;
    float velocity;
    float omega;
    float left_motor_pwm;
    float right_motor_pwm;
    uint8_t controllers_enabled;
    uint8_t feedforward_enabled;
} Controller;

/**
 * Function prototypes
 */
void Controller_Init(Controller *controller);
void Controller_EnableControllers(Controller *controller);
void Controller_DisableControllers(Controller *controller);
void Controller_ResetControllers(Controller *controller);
void Controller_Stop();

void UpdateControllers(Controller *controller, float velocity, float omega, float steering_adjustment);

float leftFeedForward(float speed);

float rightFeedForward(float speed);


#endif /* INC_CONTROLLER_H_ */
