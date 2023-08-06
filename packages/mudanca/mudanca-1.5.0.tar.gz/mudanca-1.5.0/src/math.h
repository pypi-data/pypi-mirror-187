/*
 *    This file is part of darktable,
 *    Copyright (C) 2018-2021 darktable developers.
 *
 *    darktable is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    darktable is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License
 *    along with darktable.  If not, see <http://www.gnu.org/licenses/>.
 */

#pragma once

#include <stddef.h>
#include <math.h>
#include <stdint.h>

#define NORM_MIN 1.52587890625e-05f // norm can't be < to 2^(-16)

// work around missing standard math.h symbols
/** ln(10) */
#ifndef M_LN10
#define M_LN10 2.30258509299404568402
#endif /* !M_LN10 */

/** PI */
#ifndef M_PI
#define M_PI   3.14159265358979323846
#endif /* !M_PI */
#ifndef M_PI_F
#define M_PI_F  3.14159265358979324f
#endif /* !M_PI_F */


#define DT_M_PI_F (3.14159265358979324f)
#define DT_M_PI (3.14159265358979324)

#define DT_M_LN2f (0.6931471805599453f)

// clip channel value to be between 0 and 1
// NaN-safe: NaN compares false and will result in 0.0
// also does not force promotion of floats to doubles, but will use the type of its argument
#define CLIP(x) (((x) >= 0) ? ((x) <= 1 ? (x) : 1) : 0)
#define MM_CLIP_PS(X) (_mm_min_ps(_mm_max_ps((X), _mm_setzero_ps()), _mm_set1_ps(1.0)))

// clip luminance values to be between 0 and 100
#define LCLIP(x) ((x < 0) ? 0.0 : (x > 100.0) ? 100.0 : x)

// clamp value to lie between mn and mx
// Nan-safe: NaN compares false and will result in mn
#define CLAMPF(a, mn, mx) ((a) >= (mn) ? ((a) <= (mx) ? (a) : (mx)) : (mn))
//#define CLAMPF(a, mn, mx) ((a) < (mn) ? (mn) : ((a) > (mx) ? (mx) : (a)))

// multiply 3x3 matrix with 3x1 vector
// dest needs to be different from v
#ifdef _OPENMP
#pragma omp declare simd
#endif
static inline void mat3mulv(float *const __restrict__ dest, const float *const mat, const float *const __restrict__ v)
{
  for(int k = 0; k < 3; k++)
  {
    float x = 0.0f;
    for(int i = 0; i < 3; i++)
      x += mat[3 * k + i] * v[i];
    dest[k] = x;
  }
}

// multiply two 3x3 matrices
// dest needs to be different from m1 and m2
// dest = m1 * m2 in this order
#ifdef _OPENMP
#pragma omp declare simd
#endif
static inline void mat3mul(float *const __restrict__ dest, const float *const __restrict__ m1, const float *const __restrict__ m2)
{
  for(int k = 0; k < 3; k++)
  {
    for(int i = 0; i < 3; i++)
    {
      float x = 0.0f;
      for(int j = 0; j < 3; j++)
        x += m1[3 * k + j] * m2[3 * j + i];
      dest[3 * k + i] = x;
    }
  }
}

// clang-format off
// modelines: These editor modelines have been set for all relevant files by tools/update_modelines.py
// vim: shiftwidth=2 expandtab tabstop=2 cindent
// kate: tab-indents: off; indent-width 2; replace-tabs on; indent-mode cstyle; remove-trailing-spaces modified;
// clang-format on

