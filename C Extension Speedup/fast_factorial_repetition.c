#define PY_SSIZE_T_CLEAN
#include <Python.h>

static unsigned long long c_factorial(unsigned int n) {
    unsigned long long r = 1;
    for (unsigned int i = 1; i <= n; ++i) {
        r *= i;
    }
    return r;
}

static PyObject* py_factorial_repeat_with_GIL(PyObject* self, PyObject* args) {
    unsigned int n;
    unsigned long long reps;
    if (!PyArg_ParseTuple(args, "IK", &n, &reps))
        return NULL;

    unsigned long long last = 0;

    for (unsigned long long i = 0; i < reps; ++i) {
        last = c_factorial(n);
    }

    return PyLong_FromUnsignedLongLong(last);
}

static PyObject* py_factorial_repeat_without_GIL(PyObject* self, PyObject* args) {
    unsigned int n;
    unsigned long long reps;
    if (!PyArg_ParseTuple(args, "IK", &n, &reps))
        return NULL;

    unsigned long long last = 0;

    Py_BEGIN_ALLOW_THREADS
    for (unsigned long long i = 0; i < reps; ++i) {
        last = c_factorial(n);
    }
    Py_END_ALLOW_THREADS

    return PyLong_FromUnsignedLongLong(last);
}

static PyMethodDef FastFactMethods[] = {
    {"factorial_with_GIL", py_factorial_repeat_with_GIL, METH_VARARGS,
     "Compute n! as an unsigned long long (n≤20), releasing the GIL."},
    {"factorial_without_GIL", py_factorial_repeat_without_GIL, METH_VARARGS,
     "Compute n! as an unsigned long long (n≤20), releasing the GIL."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef fastfactorialmodule = {
    PyModuleDef_HEAD_INIT,
    "fast_factorial_repetition",
    NULL,
    -1,
    FastFactMethods
};

PyMODINIT_FUNC
PyInit_fast_factorial_repetition(void)
{
    return PyModule_Create(&fastfactorialmodule);
}

