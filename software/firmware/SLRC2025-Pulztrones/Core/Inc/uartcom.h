#ifndef UARTCOM_H
#define UARTCOM_H

#include "stm32f4xx_hal.h"  // Change this depending on your STM32 series

// Function prototypes
void UART_Init(UART_HandleTypeDef *huart);    // Initialize UART
void UART_Transmit(UART_HandleTypeDef *huart, char *data);  // Transmit string data
void UART_Transmit_Float(UART_HandleTypeDef *huart, const char *header, float number, uint8_t decimal_points);  // Transmit float with customizable header
void UART_Transmit_Int(UART_HandleTypeDef *huart, const char *header, int number);  // Transmit integer with customizable header

void UART_Transmit_IR(UART_HandleTypeDef *huart, uint16_t IRL, uint16_t IRR);
void UART_Transmit_TOF(UART_HandleTypeDef *huart, uint16_t TOF1, uint16_t TOF2, uint16_t TOF3, uint16_t TOF4);


#endif /* UARTCOM_H */
