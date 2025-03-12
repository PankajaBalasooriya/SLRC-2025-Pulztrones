/**
 * @file analog_mux.h
 * @brief Header file for CD74HC4067 analog multiplexer driver
 */
#ifndef ANALOG_MUX_H
#define ANALOG_MUX_H

#include "main.h"
#include "delay.h"

/**
 * @brief Initialize the analog multiplexer
 */
void AnalogMux_Init(void);

/**
 * @brief Select a channel on the multiplexer
 * @param channel Channel number (0-15)
 */
void AnalogMux_SelectChannel(uint8_t channel);

/**
 * @brief Read the ADC value from the currently selected channel
 * @return ADC conversion result
 */
uint16_t AnalogMux_ReadADC(void);

/**
 * @brief Read ADC value from a specific channel (selects channel then reads)
 * @param channel Channel number (0-15)
 * @return ADC conversion result
 */
uint16_t AnalogMux_ReadChannel(uint8_t channel);

#endif /* ANALOG_MUX_H */
