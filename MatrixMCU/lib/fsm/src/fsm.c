/**
 * @file fsm.c
 * @brief Library to create Finite State Machines using composition.
 *
 * This library is expected to be used using composition
 * @author Teachers from the Departamento de Ingeniería Electrónica. Original authors: José M. Moya and Pedro J. Malagón. Latest contributor: Román Cárdenas.
 * @date 2023-09-20
 */

/* Includes ------------------------------------------------------------------*/
/* Standard C includes */
#include <stdlib.h>

#define FSM_MAX_TRANSITIONS 128

//GCOVR_EXCL_START
void* __attribute__((weak)) fsm_malloc(size_t s) 
{
    return malloc(s);
}

void __attribute__((weak)) fsm_free(void* p)
{
    free(p);
} 
//GCOVR_EXCL_STOP

/* Other includes */
#include "fsm.h"

static bool fsm_check_transitions(fsm_trans_t *p_tt)
{
    if (p_tt == NULL)
    {
        return false;
    }
    if ((p_tt->orig_state == -1) || (p_tt->dest_state == -1))
    {
        return false;
    }
    return true;
}

static void fsm_init_no_check(fsm_t *p_fsm, fsm_trans_t *p_tt)
{
    p_fsm->p_tt = p_tt;
    p_fsm->current_state = p_tt->orig_state;
}

fsm_t *fsm_new(fsm_trans_t *p_tt)
{
    if (!fsm_check_transitions(p_tt)) {
        return NULL;
    }
    fsm_t *p_fsm = (fsm_t *)fsm_malloc(sizeof(fsm_t));
    if (p_fsm != NULL)
    {
        fsm_init_no_check(p_fsm, p_tt);
    }
    return p_fsm;
}

void fsm_destroy(fsm_t *p_fsm)

{
    if (p_fsm != NULL) {
        fsm_free(p_fsm);
    }
    else {
        NULL;
    }
}

int fsm_init(fsm_t *p_fsm, fsm_trans_t *p_tt)
{
    int num_trans = 0;
    fsm_trans_t *p_t;

    if (p_fsm == NULL || p_tt == NULL) {
        return 0;
    }
    else {
        for (p_t = p_tt; fsm_check_transitions(p_t); ++p_t)
        {
            num_trans = num_trans + 1;
        }
    }
    if (num_trans <= FSM_MAX_TRANSITIONS){
        fsm_init_no_check(p_fsm, p_tt);
        return num_trans;
    }
    else {
        return 0;
    }
}

 int fsm_get_state(fsm_t *p_fsm)
{
    return p_fsm->current_state;
}

void fsm_set_state(fsm_t *p_fsm, int state) // GCOVR_EXCL_START
{
    p_fsm->current_state = state;
} 
// GCOVR_EXCL_STOP

int fsm_fire(fsm_t *p_fsm)
{
    fsm_trans_t *p_t;
    for (p_t = p_fsm->p_tt; p_t->orig_state >= 0; ++p_t)
    {
        if ((p_fsm->current_state == p_t->orig_state)) 
        {
            if ((p_t->in == NULL) || p_t->in(p_fsm))
            {
                p_fsm->current_state = p_t->dest_state;
                if (p_t->out)
                {
                    p_t->out(p_fsm);
                }
                return 1;
            }
            else{
                return 0;
            }
        }
    }

    return -1;

}

