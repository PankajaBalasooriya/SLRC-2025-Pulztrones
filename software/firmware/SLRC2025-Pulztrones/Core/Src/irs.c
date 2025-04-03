/*
 * irs.c
 *
 *  Created on: Apr 1, 2025
 *      Author: PANKAJA
 */
#include  "irs.h"

uint16_t IRsensorValues[16] = {0};

IR_Calibration_t IR_calibration[5] = {
    {203411.57, 14.72, -154.45},  // Front IR
	{63185.09, -1.57, 83.91},  //LEFT Front
	{70795.03, 5.63, 1.60},  //Left Back
	{93912.65, 13.94, -209.14},  //Right Back
	{78382.44, 9.55, -27.92},  //Right Front
};

void analogReadIRs(void){
	for (uint8_t i = 10; i < 15; i++)
	    {
	        IRsensorValues[i] = AnalogMux_ReadChannel(i);
	    }
}


uint16_t readRawIR(IR ir)
{
	switch(ir){
	case IR_FRONT:
		return IRsensorValues[10];
		break;
	case IR_LEFT_BACK:
		return IRsensorValues[11];
		break;
	case IR_LEFT_FORWARD:
		return IRsensorValues[12];
		break;
	case IR_RIGHT_BACK:
		return IRsensorValues[13];
		break;
	case IR_RIGHT_FORWARD:
		return IRsensorValues[14];
		break;
	default:
		return -1;
		break;
	}
}

uint16_t getIRDistance(IR ir, uint16_t raw){
	IR_Calibration_t *cal = &IR_calibration[ir];
	return (int)round(((cal->a)/(raw - cal->c)) - cal->b);
}

