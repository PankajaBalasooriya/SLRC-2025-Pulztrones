################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/Buzzer/Src/buzzer.c 

OBJS += \
./Drivers/Buzzer/Src/buzzer.o 

C_DEPS += \
./Drivers/Buzzer/Src/buzzer.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/Buzzer/Src/%.o Drivers/Buzzer/Src/%.su Drivers/Buzzer/Src/%.cyclo: ../Drivers/Buzzer/Src/%.c Drivers/Buzzer/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F446xx -c -I../Core/Inc -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/Buzzer/Inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9685/Inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/TCS3472/Inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9548A/Inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/SSD1306/Inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/core/inc" -I"D:/Oshadha/Professional Projects/SLRC 2025/Codebase/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/platform/inc" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-Buzzer-2f-Src

clean-Drivers-2f-Buzzer-2f-Src:
	-$(RM) ./Drivers/Buzzer/Src/buzzer.cyclo ./Drivers/Buzzer/Src/buzzer.d ./Drivers/Buzzer/Src/buzzer.o ./Drivers/Buzzer/Src/buzzer.su

.PHONY: clean-Drivers-2f-Buzzer-2f-Src

