#pragma once

#include "challenge-response.h"

#include <stdint.h>
// process-task
/*-------------------------------------------------------------------------------------------------------------------*/
void
cr_taskrecv_init(void);
/*-------------------------------------------------------------------------------------------------------------------*/

// process-task-response
/*-------------------------------------------------------------------------------------------------------------------*/
void
cr_taskresp_init(void);
/*-------------------------------------------------------------------------------------------------------------------*/
void
cr_taskresp_process_serial_input(const char* data);
/*-------------------------------------------------------------------------------------------------------------------*/
