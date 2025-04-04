#ifndef TASKS_H
#define TASKS_H

#include <stdint.h>
#include "config.h"


// Task definitions
typedef enum {
    TASK_PLANTATION,
    TASK_MUDDY_ROAD,
	TASK_RAMP,
    TASK_COLLECTION_POINT,
	TASK_SORTING_POTATOS,
    TASK_OLD_WAREHOUSE,
    TASK_NEW_WAREHOUSE,
    TASK_OUTDOOR,
    TASK_NONE // No active task
} TaskType;


// Function prototypes
void executePlantationTask(void);
void moveToCenterofNextCell();
void moveToCenterofCellinZeroRow();
void moveToCenterofNextCellandNotStop();


void moveToCenterofNextColumnfromFirstRow();
void moveToCenterofNextColumnfromSecondRow();
void moveToCenterofNextColumnfromThiredRow();
void moveTocolumn0Fromcolumn4();

Color picktheBall(uint8_t column, uint8_t row);


void executePotatoSeperationTask(void);




void executeMuddyRoadTask(void);
void executeCollectionPointTask(void);
void executeOldWarehouseTask(void);
void executeNewWarehouseTask(void);
void executeOutdoorTask(void);

// Task manager functions
void selectTask();
void runCurrentTask();

#endif // TASKS_H
