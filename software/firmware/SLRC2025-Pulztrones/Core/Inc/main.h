/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.h
  * @brief          : Header for main.c file.
  *                   This file contains the common defines of the application.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "stm32f4xx_hal.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */

/* USER CODE END Includes */

/* Exported types ------------------------------------------------------------*/
/* USER CODE BEGIN ET */
extern volatile uint8_t task_ready;

/* USER CODE END ET */

/* Exported constants --------------------------------------------------------*/
/* USER CODE BEGIN EC */


/* USER CODE END EC */

/* Exported macro ------------------------------------------------------------*/
/* USER CODE BEGIN EM */

/* USER CODE END EM */

void HAL_TIM_MspPostInit(TIM_HandleTypeDef *htim);

/* Exported functions prototypes ---------------------------------------------*/
void Error_Handler(void);

/* USER CODE BEGIN EFP */

/* USER CODE END EFP */

/* Private defines -----------------------------------------------------------*/
#define B1_Pin GPIO_PIN_13
#define B1_GPIO_Port GPIOC
#define B1_EXTI_IRQn EXTI15_10_IRQn
#define IR_ADC_Pin GPIO_PIN_0
#define IR_ADC_GPIO_Port GPIOC
#define AIRPUMP_Pin GPIO_PIN_1
#define AIRPUMP_GPIO_Port GPIOC
#define WATERPUMP_Pin GPIO_PIN_2
#define WATERPUMP_GPIO_Port GPIOC
#define RightEncoderCh1_Pin GPIO_PIN_0
#define RightEncoderCh1_GPIO_Port GPIOA
#define RightEncoderCh2_Pin GPIO_PIN_1
#define RightEncoderCh2_GPIO_Port GPIOA
#define USART_TX_Pin GPIO_PIN_2
#define USART_TX_GPIO_Port GPIOA
#define USART_RX_Pin GPIO_PIN_3
#define USART_RX_GPIO_Port GPIOA
#define LD2_Pin GPIO_PIN_5
#define LD2_GPIO_Port GPIOA
#define S0_Pin GPIO_PIN_12
#define S0_GPIO_Port GPIOB
#define S1_Pin GPIO_PIN_13
#define S1_GPIO_Port GPIOB
#define S2_Pin GPIO_PIN_14
#define S2_GPIO_Port GPIOB
#define S3_Pin GPIO_PIN_15
#define S3_GPIO_Port GPIOB
#define LeftEncoderCh1_Pin GPIO_PIN_8
#define LeftEncoderCh1_GPIO_Port GPIOA
#define LeftEncoderCh2_Pin GPIO_PIN_9
#define LeftEncoderCh2_GPIO_Port GPIOA
#define TMS_Pin GPIO_PIN_13
#define TMS_GPIO_Port GPIOA
#define TCK_Pin GPIO_PIN_14
#define TCK_GPIO_Port GPIOA
#define SWO_Pin GPIO_PIN_3
#define SWO_GPIO_Port GPIOB

/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
