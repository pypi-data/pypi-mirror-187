#ifndef G2O_CONFIG_H
#define G2O_CONFIG_H


/* #undef G2O_HAVE_OPENGL */
#define G2O_OPENGL_FOUND 1
/* #undef G2O_OPENMP */
/* #undef G2O_SHARED_LIBS */
/* #undef G2O_LGPL_SHARED_LIBS */

// available sparse matrix libraries
/* #undef G2O_HAVE_CHOLMOD */
/* #undef G2O_HAVE_CSPARSE */

/* #undef G2O_SINGLE_PRECISION_MATH */
#ifdef G2O_SINGLE_PRECISION_MATH
    #define G2O_NUMBER_FORMAT_STR "%g"

    #ifdef __cplusplus
        using number_t = float;
    #else
        typedef float number_t;
    #endif
#else
    #define G2O_NUMBER_FORMAT_STR "%lg"

    #ifdef __cplusplus
        using number_t = double;
    #else
        typedef double number_t;
    #endif
#endif

#define G2O_CXX_COMPILER "MSVC C:/Program Files/Microsoft Visual Studio/2022/Enterprise/VC/Tools/MSVC/14.34.31933/bin/Hostx86/x64/cl.exe"
#define G2O_SRC_DIR "D:/a/g2o-python/g2o-python/g2o"

#endif
