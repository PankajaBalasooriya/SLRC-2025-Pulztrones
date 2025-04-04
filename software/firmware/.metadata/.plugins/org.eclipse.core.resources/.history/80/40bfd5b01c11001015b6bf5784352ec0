#ifndef TASKS_H
#define TASKS_H

#include <stdint.h>
#include "config.h"


// Task definitions
typedef enum {
    TASK_PLANTATION,
	TASK_SORTING_POTATOS,
    TASK_MUDDY_ROAD,
    TASK_COLLECTION_POINT,
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

Color picktheBall(uint8_t column, uint8_t row);


void executePotatoSeperationTask(void);




void executeMuddyRoadTask(void);
void executeCollectionPointTask(void);
void executeOldWarehouseTask(void);
void executeNewWarehouseTask(void);
void executeOutdoorTask(void);

// Task manager functions
void runCurrentTask(TaskType task);

#endif // TASKS_H
