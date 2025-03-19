/**
 * @file analog_mux.c
 * @brief Implementation file for CD74HC4067 analog multiplexer driver
 */

#include "analog_mux.h"

// GPIO pin definitions for select lines
#define S0_PIN GPIO_PIN_12
#define S1_PIN GPIO_PIN_13
#define S2_PIN GPIO_PIN_14
#define S3_PIN GPIO_PIN_15
#define S_GPIO_PORT GPIOB

// External ADC handle declaration (should be defined in main.c)
extern ADC_HandleTypeDef hadc1;

/**
 * @brief Initialize the analog multiplexer
 */
void AnalogMux_Init(void)
{
    // Initialize DWT for microsecond delay
    Delay_Init();

    // S0-S3 pins are already configured as outputs in CubeMX
    // No additional initialization needed here
}

/**
 * @brief Select a channel on the multiplexer
 * @param channel Channel number (0-15)
 */
void AnalogMux_SelectChannel(uint8_t channel)
{
    // Ensure channel is within valid range (0-15)
    if (channel > 15)
        channel = 15;

    // Set S0 (least significant bit)
    if (channel & 0x01)
        HAL_GPIO_WritePin(S_GPIO_PORT, S0_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(S_GPIO_PORT, S0_PIN, GPIO_PIN_RESET);

    // Set S1
    if (channel & 0x02)
        HAL_GPIO_WritePin(S_GPIO_PORT, S1_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(S_GPIO_PORT, S1_PIN, GPIO_PIN_RESET);

    // Set S2
    if (channel & 0x04)
        HAL_GPIO_WritePin(S_GPIO_PORT, S2_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(S_GPIO_PORT, S2_PIN, GPIO_PIN_RESET);

    // Set S3 (most significant bit)
    if (channel & 0x08)
        HAL_GPIO_WritePin(S_GPIO_PORT, S3_PIN, GPIO_PIN_SET);
    else
        HAL_GPIO_WritePin(S_GPIO_PORT, S3_PIN, GPIO_PIN_RESET);

    // Add short delay for the multiplexer to settle
    // Typically 0.5-1 microsecond is enough for the CD74HC4067
    delayMicroseconds(1);
}

/**
 * @brief Read the ADC value from the currently selected channel
 * @return ADC conversion result
 */
uint16_t AnalogMux_ReadADC(void)
{
    uint16_t adcValue = 0;

    // Start ADC conversion
    HAL_ADC_Start(&hadc1);

    // Wait for conversion to complete (timeout after 100 cycles)
    if (HAL_ADC_PollForConversion(&hadc1, 100) == HAL_OK)
    {
        // Read the converted value
        adcValue = HAL_ADC_GetValue(&hadc1);
    }

    // Stop ADC conversion
    HAL_ADC_Stop(&hadc1);

    return adcValue;
}

/**
 * @brief Read ADC value from a specific channel (selects channel then reads)
 * @param channel Channel number (0-15)
 * @return ADC conversion result
 */
uint16_t AnalogMux_ReadChannel(uint8_t channel)
{
    // Select the desired channel
    AnalogMux_SelectChannel(channel);

    // Allow settling time for the analog signal
    delayMicroseconds(5);

    // Read and return the ADC value
    return AnalogMux_ReadADC();
}
