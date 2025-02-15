/*
 * encoders.c
 */

#include "main.h"
#include "encoders.h"

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
}
