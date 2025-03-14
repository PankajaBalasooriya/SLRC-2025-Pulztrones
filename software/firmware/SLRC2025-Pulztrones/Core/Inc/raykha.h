/**
 * @file RAYKHA_sensor.h
 * @brief Header file for RAYKHA-8A IR sensor array with CD74HC4067 multiplexer
 */
#ifndef RAYKHA_SENSOR_H
#define RAYKHA_SENSOR_H

#include "main.h"
#include "analog_mux.h"

// Configuration
#define RAYKHA_NUM_SENSORS          10
#define RAYKHA_DEFAULT_TIMEOUT      2500  // Timeout in microseconds (default calibration timeout)
#define RAYKHA_FIRST_MUX_CHANNEL    0     // First channel of the multiplexer used for RAYKHA
#define RAYKHA_CALIBRATION_SAMPLES  10    // Number of samples for calibration
#define TOTAL_CALIBRATION_TIME		5000  // Time for calibration in ms

// Line detection parameters
#define RAYKHA_LINE_WHITE           1     // 1 for white line on black background
#define RAYKHA_LINE_BLACK           0     // 0 for black line on white background

// Sensor calibration data structure
typedef struct {
    uint16_t min_values[RAYKHA_NUM_SENSORS];
    uint16_t max_values[RAYKHA_NUM_SENSORS];
    uint8_t line_type;
} RAYKHA_Calibration;


/**
 * @brief Read raw values from all sensors
 * @param sensor_values Array to store the raw sensor values (must be at least RAYKHA_NUM_SENSORS in size)
 */
void RAYKHA_ReadRaw(uint16_t *sensor_values);

/**
 * @brief Calibrate the sensor array
 * @param calibration Pointer to calibration data structure
 * @param line_type Type of line (RAYKHA_LINE_WHITE or RAYKHA_LINE_BLACK)
 */
void RAYKHA_Calibrate(RAYKHA_Calibration *calibration, uint8_t line_type);

/**
 * @brief Read calibrated values from all sensors
 * @param sensor_values Array to store the calibrated sensor values (must be at least RAYKHA_NUM_SENSORS in size)
 * @param calibration Pointer to calibration data structure
 */
void RAYKHA_ReadCalibrated(uint16_t *sensor_values, const RAYKHA_Calibration *calibration);

/**
 * @brief Get line position (0 to 7000) using weighted average
 * @param sensor_values Array of calibrated sensor values
 * @param calibration Pointer to calibration data structure
 * @return Line position (0 to 7000, where 0 is the leftmost sensor and 7000 is the rightmost sensor)
 *         Returns -1 if no line is detected
 */
int32_t RAYKHA_GetLinePosition(const uint16_t *sensor_values, const RAYKHA_Calibration *calibration);

/**
 * @brief Get line position for PID controller (centered around 0)
 * @param sensor_values Array of calibrated sensor values
 * @param calibration Pointer to calibration data structure
 * @return Line position centered around 0 (-3500 to 3500)
 *         Returns a large value (9999) if no line is detected
 */
int32_t RAYKHA_GetPositionForPID(const uint16_t *sensor_values, const RAYKHA_Calibration *calibration);

/**
 * @brief Check if a line is detected
 * @param sensor_values Array of calibrated sensor values
 * @param calibration Pointer to calibration data structure
 * @return 1 if line is detected, 0 otherwise
 */
uint8_t RAYKHA_IsLineDetected(const uint16_t *sensor_values, const RAYKHA_Calibration *calibration);

#endif /* RAYKHA_SENSOR_H */
