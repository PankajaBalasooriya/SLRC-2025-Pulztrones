################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.c 

OBJS += \
./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.o 

C_DEPS += \
./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.d 


# Each subdirectory must supply rules for building sources it contributes
Core/.metadata/.plugins/org.eclipse.cdt.make.core/%.o Core/.metadata/.plugins/org.eclipse.cdt.make.core/%.su Core/.metadata/.plugins/org.eclipse.cdt.make.core/%.cyclo: ../Core/.metadata/.plugins/org.eclipse.cdt.make.core/%.c Core/.metadata/.plugins/org.eclipse.cdt.make.core/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F446xx -c -I../Core/Inc -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9548A/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/SSD1306/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/core/inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/platform/inc" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f--2e-metadata-2f--2e-plugins-2f-org-2e-eclipse-2e-cdt-2e-make-2e-core

clean-Core-2f--2e-metadata-2f--2e-plugins-2f-org-2e-eclipse-2e-cdt-2e-make-2e-core:
	-$(RM) ./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.cyclo ./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.d ./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.o ./Core/.metadata/.plugins/org.eclipse.cdt.make.core/specs.su

.PHONY: clean-Core-2f--2e-metadata-2f--2e-plugins-2f-org-2e-eclipse-2e-cdt-2e-make-2e-core

