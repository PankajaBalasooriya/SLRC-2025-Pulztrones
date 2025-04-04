################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/TCS3472/Src/TCS3472.c 

OBJS += \
./Drivers/TCS3472/Src/TCS3472.o 

C_DEPS += \
./Drivers/TCS3472/Src/TCS3472.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/TCS3472/Src/%.o Drivers/TCS3472/Src/%.su Drivers/TCS3472/Src/%.cyclo: ../Drivers/TCS3472/Src/%.c Drivers/TCS3472/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F446xx -c -I../Core/Inc -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/Buzzer/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9685/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/TCS3472/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9548A/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/SSD1306/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/core/inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/platform/inc" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-TCS3472-2f-Src

clean-Drivers-2f-TCS3472-2f-Src:
	-$(RM) ./Drivers/TCS3472/Src/TCS3472.cyclo ./Drivers/TCS3472/Src/TCS3472.d ./Drivers/TCS3472/Src/TCS3472.o ./Drivers/TCS3472/Src/TCS3472.su

.PHONY: clean-Drivers-2f-TCS3472-2f-Src

