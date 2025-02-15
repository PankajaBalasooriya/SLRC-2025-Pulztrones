# SLRC 2025 Pulztrones

All project-related documents, resources, and plans are organized in the **Google Drive folder**.

[![Google Drive](https://img.shields.io/badge/Google%20Drive-Project%20Management-blue?style=for-the-badge&logo=googledrive&logoColor=white)](https://drive.google.com/drive/folders/1cOV7it_HSn0CdsOwUSD5XmdHk_gKeofi?usp=sharing)


# 📌 Pin Mapping

This document keeps track of all the **STM32F446RE Nucleo** and **Raspberry Pi 4B** pin usage.

---

## 🔌 STM32F446RE Nucleo Pin Assignments

| **Peripheral**      | **Pin**  | **Pin Setting** | **User Label** |
|--------------------|---------|---------------|--------------|
| **Motors (PWM)**  |  PB6   | TIM4_CH1 | RightMotorch1 |
|                  |  PB7  |   TIM4_CH2 | RightMotorCh2 |
|                  |  PB8  |   TIM4_CH3 | LeftMotorCh1 |
|                  |  PB9  |   TIM4_CH4 | LeftMotorCh2 |
| **Encoders**      | PA8     | TIM1_CH1 | LeftEncoderCh1     | 
|                  | PA9     | TIM1_CH2 | LeftEncoderCh2     | 
|                  | PA0     | TIM2_CH1 | RightEncoderCh1     | 
|                  | PA1     | TIM2_CH2 | RightEncoderCh2     |
---

## 🍓 Raspberry Pi 4B Pin Assignments

| **Peripheral**        | **GPIO Pin** | **Function** | **User Label** |
|----------------------|------------|-------------|--------------|


---

### ⚠️ Notes:
- **User Labels** are for easy reference in firmware.

- Keep track of any modifications and update this file accordingly.

---
  
📅 **Last Updated:** `[15-02-2025]`
