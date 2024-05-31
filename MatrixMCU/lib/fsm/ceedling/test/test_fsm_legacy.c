#include "unity.h"

#define TEST_CASE(...)
#define TEST_RANGE(...)

#include "fsm.h"
#include "mock_test_fsm.h"

#include <stdlib.h>

/**
 * @file test_fsm_legacy.c
 * @author 
 * @author 
 * @brief Tests for existing fsm module
 * @version 0.1
 * @date 2024-04-09
 * 
 */

/**
 * @brief Stub or Callback for fsm_malloc that calls real malloc. 
 * 
 * @param[in] s Amount of bytes to allocate
 * @param[in] n Amount of calls to this function
 * 
 * @return pointer to allocated memory if success; NULL if fails
 * 
 */
static void* cb_malloc(size_t s, int n) {
    return malloc(s);
}

/**
 * @brief Stub or Callback for fsm_free that calls real free. 
 * 
 * @param[in] p Pointer to allocated memory to free
 * @param[in] n Amount of calls to this function
 * 
 */
static void cb_free(void* p, int n) {
    return free(p);
}

void setUp(void)
{
}

void tearDown(void)
{
}

/**
 * @brief Comprueba que la funcion de fsm_new devuelve NULL 
 *        y no llama a fsm_malloc si la tabla de transiciones es NULL 
 */
void test_fsm_new_nullWhenNullTransition(void)
{
    fsm_t *f = (fsm_t*)1;

    f = fsm_new(NULL);

    TEST_ASSERT_EQUAL (NULL, f);
}

/**
 * @brief Comprueba que la función de inicialización devuelve false si el puntero a la maquina de estado es NULL 
 *
 */
void test_fsm_init_falseWhenNullFsm(void)
{
  fsm_trans_t tt[] = {{1, is_true, 1, do_nothing}};
  int init;
  init = fsm_init(NULL, tt);

  TEST_ASSERT_EQUAL (0, init);  

}

/**
 * @brief Función de inicializacion devuelve false si la tabla de transiciones es nula
 * 
 */
void test_fsm_init_falseWhenNullTransitions(void)
{
  fsm_t f;
  int init;
  init = fsm_init(&f, NULL);

  TEST_ASSERT_EQUAL (0, init);
}

/**
* @brief La máquina de estados devuelve NULL 
*        y no llama a fsm_malloc si el estado de origen 
*        de la primera transición es -1 (fin de la tabla)
*/
void test_fsm_nullWhenFirstOrigStateIsMinusOne (void) {
  fsm_trans_t tt[] = {{-1, is_true, 1, do_nothing}};
  fsm_t *f = (fsm_t*)1;
  f = fsm_new(tt);
 
  TEST_ASSERT_EQUAL (NULL, f);
  //TEST_FAIL_MESSAGE("Implement the test");
}

/**
 * @brief La máquina de estados devuelve NULL y no llama a fsm_malloc si el estado de destino de la primera transición es -1 (fin de la tabla)
 * 
 */
void test_fsm_nullWhenFirstDstStateIsMinusOne (void) {
  fsm_trans_t tt[] = {{1, is_true, -1, do_nothing}};
  fsm_t *f = (fsm_t*)1;
  f = fsm_new(tt);
 
  TEST_ASSERT_EQUAL (NULL, f);
  //TEST_FAIL_MESSAGE("Implement the test");
}

/**
 * @brief La máquina de estados devuelve NULL y no llama a fsm_malloc si la función de comprobación de la primera transición es NULL (fin de la tabla)
 * 
 */
/*void test_fsm_nullWhenFirstCheckFunctionIsNull (void) {
  fsm_trans_t tt[] = {{1, NULL, 1, do_nothing}};
  fsm_t *f = (fsm_t*)1;
  fsm_malloc_Stub(cb_malloc);

  f = fsm_new(tt);
 
  TEST_ASSERT_EQUAL (NULL, f);
}*/

/**
 * @brief Devuelve puntero no NULL y llama a fsm_malloc (AddCallback) al crear la maquina de estados con una transición válida con función de actualización (salida) NULL o no NULL.
 *        Hay que liberar la memoria al final llamando a free
 * 
 */
TEST_CASE(NULL)
TEST_CASE(do_nothing)
void test_fsm_new_nonNullWhenOneValidTransitionCondition(fsm_output_func_t out)
{
    fsm_trans_t tt[] = {
        {1, is_true, 2, out},
        {-1, NULL, -1, NULL}
    };
    fsm_t *f = (fsm_t*)1;
    fsm_malloc_AddCallback(cb_malloc);
    fsm_malloc_ExpectAnyArgsAndReturn(0);

    //fsm_malloc_Stub(cb_malloc);

    f = fsm_new(tt);

    // la parte de stub? fsm_new reserva el espacio de memoria ya, no?

    TEST_ASSERT_NOT_EQUAL (NULL, f);
    
    free(f);
}


/**
 * @brief Estado inicial corresponde al estado de entrada de la primera transición de la lista al crear una maquiina de estados y es valido. 
 * 
 */
void test_fsm_new_fsmGetStateReturnsOrigStateOfFirstTransitionAfterInit(void)
{
    fsm_trans_t tt[] = {{3, is_true, 1, do_nothing}};

    fsm_t *f = (fsm_t*)1;
    int res;
    fsm_malloc_Stub(cb_malloc);

    f = fsm_new(tt);
    res = fsm_get_state(f);

    TEST_ASSERT_EQUAL (3, res);

    free(f);
}

/**
 * @brief La maquina de estado no transiciona si la funcion devuelve 0
 * 
 */
void test_fsm_fire_isTrueReturnsFalseMeansDoNothingIsNotCalledAndStateKeepsTheSame(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, do_nothing},
        {-1, NULL, -1, NULL}
    };

    fsm_t f;
    int res;
    fsm_init(&f, tt);
    //is_true_ExpectAndReturn(&f,0); // ¿Como hago que is_true devuelva false? expect do_nothing?
    is_true_ExpectAnyArgsAndReturn(0); // ¿Como hago que is_true devuelva false? expect do_nothing?
    // la ausencia de un mock para comprobar do_nothing asume que no se ha producido una llamada--> no es necesario comprobar
    fsm_fire(&f);
    res = fsm_get_state(&f);

    TEST_ASSERT_EQUAL (0, res); 
}

/**
 * @brief Comprueba que el puntero pasado a fsm_fire es pasado a la función de guarda cuando se comprueba una transición
 * 
 */
void test_fsm_fire_checkFunctionCalledWithFsmPointerFromFsmFire(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, NULL},
        {-1, NULL, -1, NULL}
    };

    fsm_t *f = (fsm_t*)1;
    fsm_malloc_Stub(cb_malloc);

    f = fsm_new(tt);
    is_true_ExpectAndReturn(f,0);
    fsm_fire(f);

    free(f);

}

/** 
 * @brief Comprueba que el fsm_fire funciona y tiene el estado correcto cuando la transición devuelve true (cambia) y cuando devuelve false (mantiene)
 * 
 */
TEST_CASE(false, 0) // ¿Hay que definir otro test como el de abajo?
TEST_CASE(true, 1)
void test_fsm_fire_checkFunctionIsCalledAndResultIsImportantForTransition(bool returnValue, int expectedState)
{
    fsm_trans_t tt[] = {
        {0, is_true, expectedState, NULL},
        {-1, NULL, -1, NULL}
    };
    fsm_t f;
    bool ret;
    int state;
    fsm_init(&f, tt);
    is_true_ExpectAndReturn(&f,returnValue); 
    fsm_fire(&f);
    state = fsm_get_state(&f);

    TEST_ASSERT_EQUAL (expectedState, state);
}


/**
 * @brief La creación de una máquina de estados devuelve NULL si la reserva de memoria falla (Mock, no Stub)
 * 
 */
void test_fsm_new_nullWhenFsmMallocReturnsNull(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, NULL},
        {1, is_true, 0, NULL},
        {-1, NULL, -1, NULL}
    };
    fsm_t *f = (fsm_t*)1;
    fsm_malloc_IgnoreAndReturn(NULL);

    f = fsm_new(tt);

    TEST_ASSERT_EQUAL (NULL, f);
}

/**
 * @brief Llamar a fsm_destroy provoca una llamada a fsm_free (Mock, no Stub)
 * 
 */
void test_fsm_destroy_callsFsmFree(void)
{
    fsm_trans_t tt[] = {
    {0, is_true, 1, NULL},
    {1, is_true, 0, NULL},
    {-1, NULL, -1, NULL}
    };
    fsm_t *f = (fsm_t*)1;
    fsm_malloc_Stub(cb_malloc);
    f = fsm_new(tt);

    fsm_free_ExpectAnyArgs();
    fsm_destroy(f);

}

/**
 * @brief Comprueba que solo se llame a la función de guarda que toca según el estado actual
 * 
 */
void test_fsm_fire_callsFirstIsTrueFromState0AndThenIsTrue2FromState1(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, NULL},
        {1, is_true2, 0, NULL}, 
        {-1, NULL, -1, NULL}
    };

    fsm_t *f = (fsm_t*)1;
    int res;
    int ret;
    fsm_malloc_Stub(cb_malloc);
    f = fsm_new(tt);
    is_true_ExpectAnyArgsAndReturn(1);
    fsm_fire(f);
    res = fsm_get_state(f);

    TEST_ASSERT_EQUAL (1, res);

    is_true2_ExpectAnyArgsAndReturn(1);
    ret = fsm_fire(f);
    res = fsm_get_state(f);

    TEST_ASSERT_EQUAL(1, ret);
    TEST_ASSERT_EQUAL (0, res);

    free(f);
}

/**
 * @brief Comprueba que se pueden crear dos instancias de máquinas de estados simultánteas y son punteros distintos
 * 
 */
void test_fsm_new_calledTwiceWithSameValidDataCreatesDifferentInstancePointer(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, NULL},
        {-1, NULL, -1, NULL}
    };
    fsm_t *f = (fsm_t*)1;
    fsm_t *g = (fsm_t*)1;
    fsm_malloc_Stub(cb_malloc);
    fsm_malloc_Stub(cb_malloc);

    f = fsm_new(tt);
    g = fsm_new(tt);

    TEST_ASSERT_NOT_EQUAL (g, f);

    free(f);
    free(g);

}

// -- New tests --

/*fsm_init devuelve int con el número de transiciones
válidas (con máximo de 128 indicado en un #define
FSM_MAX_TRANSITIONS). Si es mayor, devuelve 0. */

void test_fsm_init_returniIntNumValidTransitionsEqualFSM_MAX_TRANSITIONS(void)
{
    int i;
    fsm_trans_t tti[130];
    for(i=0;i<128;i++) {
        tti[i].orig_state = 0;
        tti[i].in = is_true;
        tti[i].dest_state = 1;
        tti[i].out = do_nothing;
    }
    //tti[128] = {-1, NULL, -1, NULL};
    tti[i].orig_state = -1;
    tti[i].in = NULL;
    tti[i].dest_state = -1;
    tti[i].out = NULL;

  fsm_t f;
  int init;

  init = fsm_init(&f, tti);

  TEST_ASSERT_EQUAL (128, init);

}

void test_fsm_init_returniIntNumValidTransitionsMoreThanFSM_MAX_TRANSITIONS(void)
{
    int i;
    fsm_trans_t tti[130];
    for(i=0;i<129;i++) {
        tti[i].orig_state = 0;
        tti[i].in = is_true;
        tti[i].dest_state = 1;
        tti[i].out = do_nothing;
    }
    //tti[128] = {-1, NULL, -1, NULL};
    tti[i].orig_state = -1;
    tti[i].in = NULL;
    tti[i].dest_state = -1;
    tti[i].out = NULL;

  fsm_t f;
  int init;

  init = fsm_init(&f, tti);

  TEST_ASSERT_EQUAL (0, init);
}

/*Una función de guarda NULL en una transición equivale
a que se cumple siempre (equivale a devuelve true) */
void test_fsm_fire_NullTransitionIsTrue(void)
{
    fsm_trans_t tt[] = {
        {0, NULL, 1, do_nothing},
        {-1, NULL, -1, NULL}
    };

    fsm_t *f = (fsm_t*)1;
    int ret;
    fsm_malloc_Stub(cb_malloc);
    //is_true_ExpectAnyArgsAndReturn(NULL);
    do_nothing_ExpectAnyArgs(); 

    f = fsm_new(tt);

    ret = fsm_fire(f);

    TEST_ASSERT_EQUAL (1, ret);

    free(f);
    // Se podría hacer con do_nothing_ignore porque así se comprueba dos veces (con estado y con mock), para que se compruebe solo con estado --> ignore
}


void test_fsm_fire_ReturnIntDependingOnTransitionType(void)
{
    fsm_trans_t tt[] = {
        {0, is_true, 1, do_nothing},
        {1, is_true2, 2, do_nothing},
        {0, is_true3, 1, do_nothing},
        {-1, NULL, -1, NULL}
    };

    fsm_t f;
    int ret;
    fsm_init(&f, tt);

    is_true_ExpectAnyArgsAndReturn(1);
    do_nothing_Ignore(); 
    ret = fsm_fire(&f);
    TEST_ASSERT_EQUAL (1, ret);

    is_true2_ExpectAnyArgsAndReturn(0); 
    ret = fsm_fire(&f);
    TEST_ASSERT_EQUAL (0, ret);

    is_true2_ExpectAnyArgsAndReturn(1);
    do_nothing_Ignore(); 
    ret = fsm_fire(&f);
    TEST_ASSERT_EQUAL (1, ret);

    ret = fsm_fire(&f);
    TEST_ASSERT_EQUAL (-1, ret);

}

void test_fsm_destroy_DoesNotCallFsmFreeIfNull(void)
{
    fsm_trans_t tt[] = {
    {0, is_true, 1, NULL},
    {1, is_true, 0, NULL},
    {-1, NULL, -1, NULL}
    };
    fsm_t *f = (fsm_t*)1;
    fsm_malloc_Stub(cb_malloc);
    f = fsm_new(tt);

    fsm_destroy(NULL);

    free(f);
}
