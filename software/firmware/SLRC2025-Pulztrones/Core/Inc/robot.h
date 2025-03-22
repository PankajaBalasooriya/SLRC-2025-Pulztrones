/**
  ******************************************************************************
  * @file           : robot.h
  * @brief          : Header for robot_control.c file.
  *                   This file contains the function prototypes
  *                   for robot control operations.
  ******************************************************************************
  */

#ifndef __ROBOT_H
#define __ROBOT_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"
#include "config.h"

// In robot.h
extern int colorcounter;

/* Exported types ------------------------------------------------------------*/
/* Exported constants --------------------------------------------------------*/
/* Exported macro ------------------------------------------------------------*/
/* Exported functions prototypes ---------------------------------------------*/
void HandleLineDetection(uint8_t *data);
void HandleGridPosition(uint8_t *data);
void HandleColorDetection(uint8_t *data);
void StopRobot(void);
void HandleLineColorDetection(uint8_t *data);


//Dummy functions
//LineColor RPI_GetLineColor(uint8_t column, uint8_t row);
LineColor RPI_GetLineColor();
BallColor RPI_GetBallColor(uint8_t column, uint8_t row);



JunctionType Robot_LineFollowUntillJunction();
JunctionType Robot_LineFollowUntillJunctionAndNotStop();
void Robot_FollowLineGivenDistance(int distnace);
void Robot_FollowLineGivenDistanceandNotStop(int distnace);
JunctionType Robot_MoveForwardUntillLine();
void Robot_MoveForwardGivenDistance(int distnace);
void Robot_TurnRight90Inplace();
void Robot_TurnLeft90Inplace();


#ifdef __cplusplus
}
#endif

#endif /* __ROBOT_H */
