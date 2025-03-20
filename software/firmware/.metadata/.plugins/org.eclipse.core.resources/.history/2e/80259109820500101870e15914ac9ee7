/**
  ******************************************************************************
  * @file           : robot_control.c
  * @brief          : Robot control implementation
  *                   This file provides code for robot control operations
  ******************************************************************************
  */

/* Includes ------------------------------------------------------------------*/
#include "robot.h"
#include "config.h"
#include "sensors.h"
#include "motion.h"

extern Motion motion;


extern JunctionType junction;

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
/* Private function prototypes -----------------------------------------------*/
/* Private functions ---------------------------------------------------------*/

/**
 * @brief Handle line detection data from Raspberry Pi
 * @param data Line detection data
 */
void HandleLineDetection(uint8_t *data) {
  /* Extract line position and orientation */
  int8_t linePosition = (int8_t)data[0]; // Negative = left, Positive = right, 0 = center
  uint8_t lineAngle = data[1];           // Line angle in degrees

  /* Implement line following logic */
  if (linePosition < -20) {
    /* Turn left */
    //TurnLeft();
  } else if (linePosition > 20) {
    /* Turn right */
    //TurnRight();
  } else {
    /* Go straight */
    //MoveForward();
  }
}

/**
 * @brief Handle grid position data from Raspberry Pi
 * @param data Grid position data
 */
void HandleGridPosition(uint8_t *data) {
  /* Extract grid coordinates */
  uint8_t gridX = data[0];
  uint8_t gridY = data[1];
  uint8_t orientation = data[2]; // 0=N, 1=E, 2=S, 3=W

  /* Use grid position for navigation */
  //NavigateGrid(gridX, gridY, orientation);
}

/**
 * @brief Handle color detection data from Raspberry Pi
 * @param data Color detection data
 */
void HandleColorDetection(uint8_t *data) {
  /* Extract color information */
  uint8_t colorId = data[0]; // 0=Unknown, 1=Red, 2=Green, 3=Blue, etc.

  /* React based on color */
  switch (colorId) {
    case 1: /* Red */
      //HandleRedColor();
      break;
    case 2: /* Green */
      //HandleGreenColor();
      break;
    case 3: /* Blue */
      //HandleBlueColor();
      break;
    default:
      /* Unknown color */
      break;
  }
}




//------------------------------------------------------------------------------//
JunctionType LineFollowUntillJunction(){
	set_steering_mode(STEERING_CENTER_LINE_FOLLOW);
	Motion_StartMove(&motion, 1500, LINE_FOLLOW_SPEED, LINE_FOLLOW_SPEED, LINE_FOLLOW_ACCELERATION);
	junction = STRAIGHT_LINE;
	while(1){
		if(junction != STRAIGHT_LINE){
			break;
		}
	}
	Motion_StopAfter(&motion, 10);
	set_steering_mode(STEERING_OFF);
	return junction;

}


