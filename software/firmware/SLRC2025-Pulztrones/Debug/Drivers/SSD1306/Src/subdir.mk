################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Drivers/SSD1306/Src/bitmap.c \
../Drivers/SSD1306/Src/fonts.c \
../Drivers/SSD1306/Src/ssd1306.c 

OBJS += \
./Drivers/SSD1306/Src/bitmap.o \
./Drivers/SSD1306/Src/fonts.o \
./Drivers/SSD1306/Src/ssd1306.o 

C_DEPS += \
./Drivers/SSD1306/Src/bitmap.d \
./Drivers/SSD1306/Src/fonts.d \
./Drivers/SSD1306/Src/ssd1306.d 


# Each subdirectory must supply rules for building sources it contributes
Drivers/SSD1306/Src/%.o Drivers/SSD1306/Src/%.su Drivers/SSD1306/Src/%.cyclo: ../Drivers/SSD1306/Src/%.c Drivers/SSD1306/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F446xx -c -I../Core/Inc -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/TCS3472/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9548A/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/SSD1306/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/core/inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/platform/inc" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Drivers-2f-SSD1306-2f-Src

clean-Drivers-2f-SSD1306-2f-Src:
	-$(RM) ./Drivers/SSD1306/Src/bitmap.cyclo ./Drivers/SSD1306/Src/bitmap.d ./Drivers/SSD1306/Src/bitmap.o ./Drivers/SSD1306/Src/bitmap.su ./Drivers/SSD1306/Src/fonts.cyclo ./Drivers/SSD1306/Src/fonts.d ./Drivers/SSD1306/Src/fonts.o ./Drivers/SSD1306/Src/fonts.su ./Drivers/SSD1306/Src/ssd1306.cyclo ./Drivers/SSD1306/Src/ssd1306.d ./Drivers/SSD1306/Src/ssd1306.o ./Drivers/SSD1306/Src/ssd1306.su

.PHONY: clean-Drivers-2f-SSD1306-2f-Src

