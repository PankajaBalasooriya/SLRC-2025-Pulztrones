/*
 * systick.c
 */

#ifndef INC_SYSTICK_H_
#define INC_SYSTICK_H_

#include "main.h"

void SysTickFunction(void);

void EnableSysTickFunction(void);
void DisableSysTickFunction(void);

void CheckEncoderCounts(void);

#endif /* INC_SYSTICK_H_ */
