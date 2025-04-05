################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (13.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/arm_controller.c \
../Core/Src/ballstorage.c \
../Core/Src/box_manupilation.c \
../Core/Src/config.c \
../Core/Src/controller.c \
../Core/Src/delay.c \
../Core/Src/encoders.c \
../Core/Src/irs.c \
../Core/Src/main.c \
../Core/Src/motion.c \
../Core/Src/motors.c \
../Core/Src/profile.c \
../Core/Src/raykha.c \
../Core/Src/robot.c \
../Core/Src/sensors.c \
../Core/Src/servo.c \
../Core/Src/stm32f4xx_hal_msp.c \
../Core/Src/stm32f4xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32f4xx.c \
../Core/Src/systick.c \
../Core/Src/tasks.c \
../Core/Src/uartcom.c 

OBJS += \
./Core/Src/arm_controller.o \
./Core/Src/ballstorage.o \
./Core/Src/box_manupilation.o \
./Core/Src/config.o \
./Core/Src/controller.o \
./Core/Src/delay.o \
./Core/Src/encoders.o \
./Core/Src/irs.o \
./Core/Src/main.o \
./Core/Src/motion.o \
./Core/Src/motors.o \
./Core/Src/profile.o \
./Core/Src/raykha.o \
./Core/Src/robot.o \
./Core/Src/sensors.o \
./Core/Src/servo.o \
./Core/Src/stm32f4xx_hal_msp.o \
./Core/Src/stm32f4xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32f4xx.o \
./Core/Src/systick.o \
./Core/Src/tasks.o \
./Core/Src/uartcom.o 

C_DEPS += \
./Core/Src/arm_controller.d \
./Core/Src/ballstorage.d \
./Core/Src/box_manupilation.d \
./Core/Src/config.d \
./Core/Src/controller.d \
./Core/Src/delay.d \
./Core/Src/encoders.d \
./Core/Src/irs.d \
./Core/Src/main.d \
./Core/Src/motion.d \
./Core/Src/motors.d \
./Core/Src/profile.d \
./Core/Src/raykha.d \
./Core/Src/robot.d \
./Core/Src/sensors.d \
./Core/Src/servo.d \
./Core/Src/stm32f4xx_hal_msp.d \
./Core/Src/stm32f4xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32f4xx.d \
./Core/Src/systick.d \
./Core/Src/tasks.d \
./Core/Src/uartcom.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F446xx -c -I../Core/Inc -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/Buzzer/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9685/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/TCS3472/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/PCA9548A/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/SSD1306/Inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/core/inc" -I"C:/Users/PANKAJA/OneDrive/Projects/SLRC/SLRC-2025-Pulztrones/software/firmware/SLRC2025-Pulztrones/Drivers/VL53L0X/platform/inc" -I../Drivers/STM32F4xx_HAL_Driver/Inc -I../Drivers/STM32F4xx_HAL_Driver/Inc/Legacy -I../Drivers/CMSIS/Device/ST/STM32F4xx/Include -I../Drivers/CMSIS/Include -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/arm_controller.cyclo ./Core/Src/arm_controller.d ./Core/Src/arm_controller.o ./Core/Src/arm_controller.su ./Core/Src/ballstorage.cyclo ./Core/Src/ballstorage.d ./Core/Src/ballstorage.o ./Core/Src/ballstorage.su ./Core/Src/box_manupilation.cyclo ./Core/Src/box_manupilation.d ./Core/Src/box_manupilation.o ./Core/Src/box_manupilation.su ./Core/Src/config.cyclo ./Core/Src/config.d ./Core/Src/config.o ./Core/Src/config.su ./Core/Src/controller.cyclo ./Core/Src/controller.d ./Core/Src/controller.o ./Core/Src/controller.su ./Core/Src/delay.cyclo ./Core/Src/delay.d ./Core/Src/delay.o ./Core/Src/delay.su ./Core/Src/encoders.cyclo ./Core/Src/encoders.d ./Core/Src/encoders.o ./Core/Src/encoders.su ./Core/Src/irs.cyclo ./Core/Src/irs.d ./Core/Src/irs.o ./Core/Src/irs.su ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su ./Core/Src/motion.cyclo ./Core/Src/motion.d ./Core/Src/motion.o ./Core/Src/motion.su ./Core/Src/motors.cyclo ./Core/Src/motors.d ./Core/Src/motors.o ./Core/Src/motors.su ./Core/Src/profile.cyclo ./Core/Src/profile.d ./Core/Src/profile.o ./Core/Src/profile.su ./Core/Src/raykha.cyclo ./Core/Src/raykha.d ./Core/Src/raykha.o ./Core/Src/raykha.su ./Core/Src/robot.cyclo ./Core/Src/robot.d ./Core/Src/robot.o ./Core/Src/robot.su ./Core/Src/sensors.cyclo ./Core/Src/sensors.d ./Core/Src/sensors.o ./Core/Src/sensors.su ./Core/Src/servo.cyclo ./Core/Src/servo.d ./Core/Src/servo.o ./Core/Src/servo.su ./Core/Src/stm32f4xx_hal_msp.cyclo ./Core/Src/stm32f4xx_hal_msp.d ./Core/Src/stm32f4xx_hal_msp.o ./Core/Src/stm32f4xx_hal_msp.su ./Core/Src/stm32f4xx_it.cyclo ./Core/Src/stm32f4xx_it.d ./Core/Src/stm32f4xx_it.o ./Core/Src/stm32f4xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su ./Core/Src/system_stm32f4xx.cyclo ./Core/Src/system_stm32f4xx.d ./Core/Src/system_stm32f4xx.o ./Core/Src/system_stm32f4xx.su ./Core/Src/systick.cyclo ./Core/Src/systick.d ./Core/Src/systick.o ./Core/Src/systick.su ./Core/Src/tasks.cyclo ./Core/Src/tasks.d ./Core/Src/tasks.o ./Core/Src/tasks.su ./Core/Src/uartcom.cyclo ./Core/Src/uartcom.d ./Core/Src/uartcom.o ./Core/Src/uartcom.su

.PHONY: clean-Core-2f-Src

