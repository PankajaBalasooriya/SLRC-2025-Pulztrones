/*
 * systick.c
 */

#include "main.h"
// #include "pid.h"
#include "encoders.h"
#include "uartcom.h"
#include "motion.h"
#include "sensors.h"
#include "arm_controller.h"
#include "robot.h"

extern Motion motion;

extern volatile uint8_t systick_function_enabled;
extern UART_HandleTypeDef huart3;

void SysTickFunction(void) {
	/*
	 * Anything in this function body will be executed every millisecond.
	 * Call you PID update function here.
	 */
	//--------------------------------------------------------------------
		update_Encoder_Data();
		Motion_Update(&motion);
		Sensors_Update();

		UpdateControllers(&controller, Motion_Velocity(&motion), Motion_Omega(&motion), get_steering_feedback());
		//UpdateControllers(&controller, Motion_Velocity(&motion), Motion_Omega(&motion), 0);
	//--------------------------------------------------------------------
		//UART_Transmit_EncoderData(&huart3);

		//UART_Transmit_Int(&huart3, "L", linecolorRPI);
		//UART_Transmit_Int(&huart3, "B", ballcolorRPI);



}



void EnableSysTickFunction(void) {
  //HAL_Delay(10);
  systick_function_enabled = 1;
  HAL_Delay(10);
}

void DisableSysTickFunction(void) {
	//HAL_Delay(10);
  systick_function_enabled = 0;
  HAL_Delay(10);
}

void CheckEncoderCounts(void){
	/*
		 * This code prevents PID errors when the encoder counts get too high. For example, without it then
		 * if the wheels are spinning forwards and PID is trying to keep their encoder counts equal, and one of the wheels
		 * turns past 32767 and its encoder counts loop back to -32768, suddenly the difference between the encoder counts
		 * is massive and the wheels will start spinning at full speed in opposite directions to even back out.
		 *
		 * This code helps prevent that by reseting the encoder counts when any of the encoder values get too extreme.
		 * It also maintains the magnitude of the difference between the left and right encoders so that PID will work seamlessly.
		 *
		 * You may have to adjust it in the event you try to traverse more than 31000 encoder counts at once (~9 meters) without
		 * turning. But that'll be approximately never in Micromouse :)
		 */
		if (getRightEncoderCounts() > 31000 || getLeftEncoderCounts() > 31000
				|| getRightEncoderCounts() < -31000 || getLeftEncoderCounts() < -31000) {
			int16_t difference = getRightEncoderCounts() - getLeftEncoderCounts();
			resetEncodersinSystick();
			TIM1->CNT = (int16_t) difference;
		}
}
