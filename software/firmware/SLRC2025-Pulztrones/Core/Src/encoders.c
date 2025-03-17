/*
 * encoders.c
 */

#include "main.h"
#include "encoders.h"
#include "config.h"
#include "uartcom.h"

extern UART_HandleTypeDef huart3;

volatile float m_robot_distance = 0;
volatile float m_robot_angle = 0;

int16_t left_delta = 0;
int16_t right_delta = 0;
int16_t previous_left_count = 0;
int16_t previous_right_count = 0;

float m_fwd_change = 0;
float m_rot_change = 0;



/*
 * NOTE: your timers might be different based on what you used when designing your PCB!
 * Also, if your encoder values are negative of what they should be, multiply the return values by -1.
 */

int16_t getRightEncoderCounts() {
	return (int16_t) TIM2->CNT;
}

int16_t getLeftEncoderCounts() {
	return (int16_t) TIM1->CNT;
}

void resetEncoders() {
	TIM1->CNT = (int16_t) 0;
	TIM2->CNT = (int16_t) 0;
	m_robot_distance = 0;
	m_robot_angle = 0;
	left_delta = 0;
	right_delta = 0;
	previous_left_count = 0;
	previous_right_count = 0;

}

void resetEncodersinSystick() {
	TIM1->CNT = (int16_t) 0;
	TIM2->CNT = (int16_t) 0;
}

void update_Encoder_Data(){
	int16_t left_count = getLeftEncoderCounts();
	int16_t right_count = getRightEncoderCounts();

	left_delta = left_count - previous_left_count;
	previous_left_count = left_count;

	right_delta = right_count - previous_right_count;
	previous_right_count = right_count;

	float left_change = left_delta * MM_PER_COUNT_LEFT;
	float right_change = right_delta * MM_PER_COUNT_RIGHT;

	m_fwd_change = 0.5 * (right_change + left_change);
	m_robot_distance += m_fwd_change;
	m_rot_change = (right_change - left_change) * DEG_PER_MM_DIFFERENCE;
	m_robot_angle += m_rot_change;


}

float robot_distance() {
    float distance;
    distance = m_robot_distance;
    return distance;
}

float robot_speed() {// in mms-1
	float speed;
	speed = LOOP_FREQUENCY * m_fwd_change;
	return speed;
}

float robot_omega() {//in degs-1
	float omega;
	omega = LOOP_FREQUENCY * m_rot_change;
	return omega;
}

float robot_fwd_change() {
	float distance;
	distance = m_fwd_change;
	return distance;
}

float robot_rot_change() {
	float distance;
	distance = m_rot_change;
	return distance;
}

float robot_angle() {
	float angle;
	angle = m_robot_angle;
	return angle;
}



