/**
  ******************************************************************************
  * @file           : RPI_uart_comm.h
  * @brief          : Header for uart_comm.c file.
  *                   This file contains the common defines and function prototypes
  *                   for UART communication with Raspberry Pi.
  ******************************************************************************
  */

#ifndef __RPI_UART_COMM_H
#define __RPI_UART_COMM_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Exported types ------------------------------------------------------------*/
/* Communication protocol definitions */
#define START_MARKER '<'
#define END_MARKER '>'
#define MAX_BUFFER_SIZE 128

/* Command IDs */
#define CMD_LINE_DETECTED 0x01
#define CMD_GRID_POSITION 0x02
#define CMD_COLOR_DETECTED 0x03
#define CMD_START_LINE_FOLLOWING 0x11
#define CMD_START_GRID_NAVIGATION 0x12
#define CMD_START_TASK_1_COLOR_DETECTION 0x13
#define CMD_STOP 0x20

/* Reception state machine */
typedef enum {
  WAITING_FOR_START,
  WAITING_FOR_CMD,
  WAITING_FOR_LENGTH,
  RECEIVING_DATA,
  WAITING_FOR_END
} RxState;

/* Exported variables */
extern UART_HandleTypeDef huart6;
extern RxState rxState;
extern uint8_t rxBuffer[];
extern uint8_t rxCmd;
extern uint8_t rxLength;
extern uint8_t rxIndex;
extern uint8_t rxByte;

/* Exported functions prototypes ---------------------------------------------*/
void RPI_UART_Init(void);
void ProcessCommand(void);
void SendCommand(uint8_t cmd, uint8_t *data, uint8_t length);
void StartLineFollowing(void);
void StartGridNavigation(uint8_t targetX, uint8_t targetY);
void StartColorDetection(void);
void StopProcessing(void);

#ifdef __cplusplus
}
#endif

#endif /* __RPI_UART_COMM_H */
